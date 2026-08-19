"""Deterministic, traceable preprocessing for book text sent to TTS backends.

The compiler operates on structured FB2-derived chapters and paragraphs before
sentence segmentation.  It deliberately keeps backend-specific Silero syntax
(stress marks and safe wrapper hardening) behind one explicit stage instead of
spreading book rules through the backend implementation.
"""

from __future__ import annotations

import json
import logging
import re
import tomllib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Pattern, Tuple

from .fb2_parser import ParsedBook

logger = logging.getLogger(__name__)
_COMPAT_LOGGER = logging.getLogger("src.core.tts_silero")

PROJECT_PRONUNCIATIONS_PATH = Path(__file__).resolve().parent.parent.parent / "pronunciations.toml"
PRONUNCIATIONS_PATH = Path.home() / ".audiobook-generator" / "pronunciations.toml"
PronunciationRule = Tuple[Pattern[str], str]

_MASKED_ASTERISKS_RE = re.compile(
    r"\*(?:-\*)+|(?<!\*)\*{2,}(?!\*)|(?<=\w)\*(?=\w)"
)
_IDENTIFIER_WITH_LEADING_ZERO_RE = re.compile(
    r"(?<!\d)(\d+)([-−–])0(\d+)(?!\d)"
)
_CLOCK_RE = re.compile(r"(?<!\d)([01]?\d|2[0-3])\.([0-5]\d)(?!\d)")
_CLOCK_CONTEXT_RE = re.compile(
    r"(?:\b(?:в|к|до|после|около)|\b(?:выезд|вылет|начало|подъём|подъем))\s*$",
    flags=re.IGNORECASE,
)
_RU_DIGIT_WORDS = (
    "ноль", "один", "два", "три", "четыре",
    "пять", "шесть", "семь", "восемь", "девять",
)

_BROKEN_RU_ABBREVIATION_PATTERNS = {
    r"д.\s*н.\s*э.": r"(?<!\w)д\.\s*н\.\s*э\.(?!\w)",
    r"н.\s*э.": r"(?<!\w)н\.\s*э\.(?!\w)",
}
_ELONGATED_VOWEL_RE = re.compile(
    r"(?P<vowel>[аеёиоуыэюя])(?:[-–—](?P=vowel))+|"
    r"(?P<plain>[аеёиоуыэюя])(?P=plain){2,}",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class AcronymDecision:
    token: str
    mode: str
    output: str


def resolve_acronym(
    token: str,
    *,
    spell_letters: Iterable[str] = (),
    lexicalized_words: Iterable[str] = (),
) -> AcronymDecision:
    """Resolve only explicit acronym entries; unknown tokens stay unchanged."""
    if token in set(spell_letters):
        return AcronymDecision(token, "spell_letters", " ".join(token))
    if token in set(lexicalized_words):
        return AcronymDecision(token, "lexicalized_word", token)
    return AcronymDecision(token, "unknown", token)


def detect_expressive_elongations(text: str) -> List[Dict[str, Any]]:
    """Detect expressive vowel spellings without changing production text."""
    return [
        {"text": match.group(0), "start": match.start(), "end": match.end(),
         "status": "experimental"}
        for match in _ELONGATED_VOWEL_RE.finditer(text)
    ]


@dataclass(frozen=True)
class ChangeRecord:
    rule_id: str
    original: str
    normalized: str
    chapter: int
    paragraph: int
    segment_id: Optional[str]
    source_id: str
    source_offsets: Optional[Tuple[int, int]]
    category: str
    reason: str


@dataclass
class NormalizedChapter:
    index: int
    title: str
    paragraphs: List[str]
    paragraph_ids: List[str]


@dataclass
class NormalizedBook:
    title: str
    language: str
    chapters: List[NormalizedChapter]
    changes: List[ChangeRecord] = field(default_factory=list)


def harden_silero_ru_preprocessing(language_data: Optional[dict] = None) -> None:
    """Correct unsafe abbreviation regexes in the installed Silero wrapper."""
    if language_data is None:
        from silero_tts.lang_data import lang_data

        language_data = lang_data
    ru_patterns = language_data.get("ru", {}).get("patterns", [])
    language_data["ru"]["patterns"] = [
        (_BROKEN_RU_ABBREVIATION_PATTERNS.get(pattern, pattern), replacement)
        for pattern, replacement in ru_patterns
    ]


def load_pronunciations(path: Optional[Path] = None) -> List[PronunciationRule]:
    """Load merged project/user Silero pronunciation rules."""
    merged_ru_entries: Dict[str, str] = {}
    paths_to_load: List[Path] = []
    if PROJECT_PRONUNCIATIONS_PATH.exists():
        paths_to_load.append(PROJECT_PRONUNCIATIONS_PATH)
    custom_path = Path(path) if path is not None else PRONUNCIATIONS_PATH
    if custom_path not in paths_to_load and custom_path.exists():
        paths_to_load.append(custom_path)

    for source_path in paths_to_load:
        try:
            with source_path.open("rb") as file:
                data = tomllib.load(file)
            ru_entries = data.get("ru", {})
            if isinstance(ru_entries, dict):
                for source, replacement in ru_entries.items():
                    if source and isinstance(replacement, str):
                        merged_ru_entries[source] = replacement
        except (OSError, tomllib.TOMLDecodeError) as exc:
            logger.warning("не удалось загрузить словарь произношений %s: %s", source_path, exc)
            if _COMPAT_LOGGER is not logger:
                _COMPAT_LOGGER.warning(
                    "не удалось загрузить словарь произношений %s: %s", source_path, exc,
                )

    entries = sorted(merged_ru_entries.items(), key=lambda item: len(item[0]), reverse=True)
    return [
        (re.compile(rf"(?<!\w){re.escape(source)}(?!\w)", re.IGNORECASE), replacement)
        for source, replacement in entries
    ]


def apply_pronunciations(text: str, rules: List[PronunciationRule]) -> str:
    """Apply dictionary rules without losing the first matched capital."""
    def replace_match(match: re.Match[str], replacement: str) -> str:
        matched_first = next((char for char in match.group(0) if char.isalpha()), "")
        if not matched_first.isupper():
            return replacement
        for index, char in enumerate(replacement):
            if char.isalpha():
                return replacement[:index] + char.upper() + replacement[index + 1:]
        return replacement

    result = text
    for pattern, replacement in rules:
        result = pattern.sub(
            lambda match, value=replacement: replace_match(match, value), result,
        )
    return result


def resolve_vse_vsyo_homographs(text: str) -> str:
    """Resolve only evidenced ``все``/``всё`` contexts."""
    text = re.sub(r"\b([Вв])се(-таки\b|\s+-?\(?таки\b)", r"\g<1>сё\2", text)
    text = re.sub(r"\b([Вв])се(\s+равно\b)", r"\g<1>сё\2", text)
    text = re.sub(r"\b([Вв])се(\s+так\s+же\b)", r"\g<1>сё\2", text)
    text = re.sub(r"\b([Вв])се(\s+время\b)", r"\g<1>сё\2", text)
    text = re.sub(r"\b([Вв])се(\s+ещ[её]\b)", r"\g<1>сё\2", text)
    text = re.sub(r"\b([Вв])се(\s+всерь[её]з\b)", r"\g<1>сё\2", text)
    text = re.sub(
        r"\b([Вв])се(\s+(?:больше|меньше|проще|дальше|чаще|ближе|тяжелее|сильнее|лучше|хуже|дороже|дешевле|быстрее|медленнее|выше|ниже|глубже)\b)",
        r"\g<1>сё\2", text,
    )
    text = re.sub(
        r"\b([Вв])се(\s+(?:это|этого|этому|этим|этом|то|того|тому|тем|том|остальное|остального|необходимое|прочее)\b)",
        r"\g<1>сё\2", text,
    )
    text = re.sub(r"\b([Вв])се(\s+самое\b)", r"\g<1>сё\2", text)

    def fix_zhe(match: re.Match[str]) -> str:
        word, rest = match.group(1), match.group(2)
        prefix = text[:match.start()].rstrip()
        conjunction = re.search(r"(?:^|\s)(но|и|а|как|где|хотя|даже|так)\s*$", prefix, re.I)
        after_text = text[match.end():].strip()
        words = re.findall(r"\b[^\s,.!?:;—–\-«»\"'()]+\b", after_text)
        has_plural_noun = any(
            word.endswith(("ия", "ы", "и", "а")) for word in words[:2]
        )
        has_plural_verb = any(
            word.endswith(("ли", "лись", "ют", "ут", "ят", "ат"))
            for word in words[1:5]
        )
        if has_plural_noun and has_plural_verb and not conjunction:
            return f"{'Вс+е' if word[0].isupper() else 'вс+е'}{rest}"
        return f"{'Всё' if word[0].isupper() else 'всё'}{rest}"

    text = re.sub(r"\b([Вв]се)(\s+же?\b)", fix_zhe, text)
    text = re.sub(
        r"\b([Вв]се)(\s+(?:[а-яёА-ЯЁ]+(?:ли|лись|ют|ут|ят|ат)\b))",
        lambda match: f"{'Вс+е' if match.group(1)[0].isupper() else 'вс+е'}{match.group(2)}",
        text,
    )
    return re.sub(r"\b([Оо]дин)\s+в\s+один\b", r"\g<1> в од+ин", text)


def prepare_silero_text(text: str) -> str:
    """Apply deterministic Silero-safe punctuation and number preparation."""
    def replace_mask(match: re.Match[str]) -> str:
        before = text[:match.start()].rstrip("-")[-1:]
        after = text[match.end():].lstrip("-")[:1]
        return "…" if before.isalnum() or after.isalnum() else "пик"

    result = resolve_vse_vsyo_homographs(text)
    result = _MASKED_ASTERISKS_RE.sub(replace_mask, result)
    result = _IDENTIFIER_WITH_LEADING_ZERO_RE.sub(
        lambda match: f"{match.group(1)} дефис "
        f"{' '.join(_RU_DIGIT_WORDS[int(digit)] for digit in '0' + match.group(3))}",
        result,
    )

    def replace_clock(match: re.Match[str]) -> str:
        prefix = result[:match.start()]
        hour = match.group(1)
        if not hour.startswith("0") and not _CLOCK_CONTEXT_RE.search(prefix):
            return match.group(0)
        return f"{int(hour)} {match.group(2)}"

    result = _CLOCK_RE.sub(replace_clock, result)
    result = result.replace("⁈", "?!")
    return re.sub(r"[ \t]+", " ", result).strip()


def _replace_phrase(text: str, pattern: str, replacement: Any) -> str:
    def replace(match: re.Match[str]) -> str:
        value = replacement(match) if callable(replacement) else match.expand(replacement)
        first_alpha = next((char for char in match.group(0) if char.isalpha()), "")
        if not first_alpha.isupper():
            return value
        for index, char in enumerate(value):
            if char.isalpha():
                return value[:index] + char.upper() + value[index + 1:]
        return value

    return re.sub(pattern, replace, text, flags=re.IGNORECASE)


class TtsPreprocessor:
    """Compile structured book text into normalized deterministic TTS text."""

    def __init__(self, *, backend: str = "silero", profile: str = "") -> None:
        self.backend = backend
        self.profile = profile.casefold()
        self._language = "ru"
        self._rules = load_pronunciations()

    def normalize_text(
        self,
        text: str,
        *,
        chapter: int,
        paragraph: int,
        source_id: str,
        changes: List[ChangeRecord],
    ) -> str:
        if self.backend != "silero" or self._language != "ru":
            return text

        result = text
        dictionary_result = apply_pronunciations(result, self._rules)
        if dictionary_result != result:
            changes.append(ChangeRecord(
                rule_id="lexicon.project",
                original=result,
                normalized=dictionary_result,
                chapter=chapter,
                paragraph=paragraph,
                segment_id=None,
                source_id=source_id,
                source_offsets=None,
                category="lexical stress / proper name",
                reason="merged project and user pronunciation dictionary",
            ))
        result = dictionary_result
        result = self._apply_context_rules(result, chapter, paragraph, source_id, changes)
        prepared = prepare_silero_text(result)
        if prepared != result:
            changes.append(ChangeRecord(
                rule_id="silero.preprocessing",
                original=result,
                normalized=prepared,
                chapter=chapter,
                paragraph=paragraph,
                segment_id=None,
                source_id=source_id,
                source_offsets=None,
                category="backend preprocessing",
                reason="deterministic Silero input normalization",
            ))
        return prepared

    def _apply_context_rules(
        self,
        text: str,
        chapter: int,
        paragraph: int,
        source_id: str,
        changes: List[ChangeRecord],
    ) -> str:
        result = text

        def apply(rule_id: str, pattern: str, replacement: str, category: str, reason: str) -> None:
            nonlocal result
            updated = _replace_phrase(result, pattern, replacement)
            if updated != result:
                changes.append(ChangeRecord(
                    rule_id=rule_id,
                    original=result,
                    normalized=updated,
                    chapter=chapter,
                    paragraph=paragraph,
                    segment_id=None,
                    source_id=source_id,
                    source_offsets=None,
                    category=category,
                    reason=reason,
                ))
                result = updated

        apply("phrase.two_and_half_hours", r"\bдва с половиной часа\b", "два с половиной час+а", "inflection", "genitive singular after quantity")
        apply("phrase.nabralos", r"\bнабралось\b", "набрал+ось", "lexical stress", "confirmed listening form")
        apply("phrase.ne_bylo", r"\b(никого|вопросов) не было\b", r"\1 н+е было", "phrase stress", "negative existential construction")
        apply("phrase.potom", r"\b(а|и) потом\b", r"\1 пот+ом", "homograph", "temporal conjunction; do not rewrite sweat instrumental")
        apply("phrase.eyes", r"\b(открывать|поднял) глаза\b", r"\1 глаз+а", "syntax-government", "confirmed phrase reading")
        apply("phrase.royal_statyu", r"\bс королевской статью\b", "с королевской ст+атью", "syntax-government", "instrumental form in confirmed phrase")
        apply("phrase.ne_s_chem", r"\bне с чем\b", "н+е с чем", "phrase stress", "negative construction")
        apply("phrase.vysoty", r"\bЯ высоты боюсь\b", "Я высот+ы боюсь", "syntax-government", "бояться чего")
        apply("phrase.strelku", r"\bпока стрелку не надоест\b", "пока стрелк+у не надоест", "syntax-government", "кому не надоест")
        apply("phrase.hlopok", r"\bхлопок вышибного заряда\b", "хлоп+ок вышибного заряда", "homograph", "sound/charge meaning")
        apply("phrase.steny", r"\bв сторону стены\b", "в сторону стен+ы", "syntax-government", "в сторону чего")
        apply("phrase.napadavshih", r"\bчетверо нападавших\b", "четверо напад+авших", "inflection", "confirmed participle form")
        apply("phrase.rodov", r"\bпредставители великих родов\b", "представители великих род+ов", "homograph", "lineage meaning")
        apply("phrase.litsa", r"\bкрасноте лица\b", "красноте лиц+а", "syntax-government", "красноте чего")
        apply("phrase.medium_day", r"\bв среду(?!\s+(?:обитания|окружение|среда))\b", "в ср+еду", "homograph", "day-of-week reading")
        apply("phrase.medium_day_context", r"\b(провод\w+)\s+(свою\s+)?среду\b", r"\1 \2ср+еду", "homograph", "day-of-week object in a bounded conduct-schedule construction")
        apply("phrase.lock", r"\b(дверной|навесной|висячий) замок\b", r"\1 зам+ок", "homograph", "lock meaning; preserve the modifier")
        apply("phrase.lock_context", r"\bзамок(?=\s+(?:явно\s+)?не\s+желал\s+открываться\b)", "зам+ок", "homograph", "lock meaning from bounded opening context")
        apply("phrase.lock_after_key", r"(\bключ,\s+но\s+)замок\b", r"\1зам+ок", "homograph", "lock meaning after an explicit key contrast")
        if self.profile and ("book9" in self.profile or "гимн шута" in self.profile):
            apply("project.galitsyn", r"\bГалицын(?:а|у|ым|е)?\b", self._galitsyn_replacement, "proper name", "explicit book profile pronunciation")
        return result

    @staticmethod
    def _galitsyn_replacement(match: re.Match[str]) -> str:
        suffix = match.group(0)[7:]
        return "Гал+ицын" + suffix

    def compile_book(self, book: ParsedBook) -> NormalizedBook:
        self._language = book.metadata.lang.casefold()[:2]
        changes: List[ChangeRecord] = []
        chapters: List[NormalizedChapter] = []
        for chapter_index, chapter in enumerate(book.chapters, start=1):
            title_id = f"ch-{chapter_index:04d}-title"
            title = self.normalize_text(
                chapter.title,
                chapter=chapter_index,
                paragraph=0,
                source_id=title_id,
                changes=changes,
            )
            paragraphs: List[str] = []
            paragraph_ids: List[str] = []
            for paragraph_index, paragraph in enumerate(chapter.paragraphs, start=1):
                source_id = f"ch-{chapter_index:04d}-p-{paragraph_index:04d}"
                paragraph_ids.append(source_id)
                paragraphs.append(self.normalize_text(
                    paragraph,
                    chapter=chapter_index,
                    paragraph=paragraph_index,
                    source_id=source_id,
                    changes=changes,
                ))
            chapters.append(NormalizedChapter(
                index=chapter_index,
                title=title,
                paragraphs=paragraphs,
                paragraph_ids=paragraph_ids,
            ))
        return NormalizedBook(book.metadata.title, book.metadata.lang, chapters, changes)


def write_tts_artifacts(
    normalized: NormalizedBook,
    output_dir: Path,
    stem: str,
    *,
    segments: Optional[Iterable[Dict[str, Any]]] = None,
) -> Tuple[Path, Path]:
    """Persist a readable normalized script and machine-readable trace."""
    output_dir.mkdir(parents=True, exist_ok=True)
    script_path = output_dir / f"{stem}.tts.md"
    changes_path = output_dir / f"{stem}.tts-changes.json"
    segment_rows = list(segments or [])

    lines = [f"# TTS script: {normalized.title or stem}", "", "<!-- generated; Markdown is not sent to TTS -->", ""]
    for chapter in normalized.chapters:
        lines.extend([f"## Chapter {chapter.index}: {chapter.title or '(untitled)'}", ""])
        for paragraph_index, (paragraph_id, text) in enumerate(zip(chapter.paragraph_ids, chapter.paragraphs), start=1):
            lines.extend([f"### {paragraph_id}", "", text, ""])
            paragraph_segments = [row for row in segment_rows if row.get("source_paragraph") == paragraph_id]
            for row in paragraph_segments:
                lines.append(
                    f"- `{row['segment_id']}` boundary=`{row['boundary_before']}`: {row['text']}"
                )
            if paragraph_segments:
                lines.append("")
    script_path.write_text("\n".join(lines), encoding="utf-8")

    payload = {
        "schema_version": 1,
        "book_title": normalized.title,
        "language": normalized.language,
        "changes": [asdict(change) for change in normalized.changes],
        "segments": segment_rows,
    }
    changes_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return script_path, changes_path
