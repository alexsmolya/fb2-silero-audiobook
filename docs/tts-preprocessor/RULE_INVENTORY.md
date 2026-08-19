# TTS preprocessing rule inventory

Inventory reconciled before implementation on 2026-08-19 from:

- local Git history and current `main` (`9fd35745ba294bd455307e90144b20169d52ee34`);
- current Python/TOML code and regression tests;
- local Codex reports, run logs, `docs/TTS_QUALITY_LOG.md`, and `docs/LOCAL_CHANGES.md`;
- `docs/upstream-findings/README.md`;
- Drive journal `2026-08-18_audiobook_generator_tts_preprocessor_plan`;
- Drive handoffs `2026-08-14_audiobook_generator_vse_vsyo_homograph_audit.md`,
  `2026-08-14_audiobook_generator_pronunciation_fix_phase2.md`, and
  `2026-08-14_audiobook_generator_pronunciation_release.md`.

This is an engineering inventory, not a transcript. “Current location” points to
the implementation that exists before consolidation. “Destination” is the target
owned by the explicit preprocessing/compiler stage. `implemented now` describes
the baseline before this feature branch.

## Status legend

- `confirmed`: supported by a regression test and/or accepted listening evidence;
- `observed`: listening or forensic observation with a narrower current scope;
- `experimental`: architecture/test corpus only; no production rewrite;
- `unresolved`: no safe production rule has been accepted yet.

| ID / example | Expected normalized/read form | Class | Implemented now? / current location | Destination and scope | Negative controls | Status |
|---|---|---|---|---|---|---|
| `heading-number`: `Глава 16` | `Глава шестнадцатая` | structural FB2 / lexical | YES, `pronunciations.toml` | compiler structural heading rule; safe global for supported chapter numbers | ordinary `Глава` text; body heading repeated later | confirmed |
| `demidovich`: `Демидович`, case forms | `Дем+идович`, corresponding forms | proper name | YES, `pronunciations.toml` | safe lexicon entry | unrelated `Демидов` names | confirmed |
| `pasha`: `Паша`, case forms | `П+аша`, corresponding forms | proper name | YES, `pronunciations.toml` | safe lexicon entry | unrelated words containing `паша` | confirmed |
| `klanovka`: `клановка`, forms | `кл+ановка`, corresponding forms | proper name / lexical stress | YES, `pronunciations.toml` | safe lexicon entry | other `клан` words | confirmed |
| `yastreb`: `ястребами`, `ястребов`, `ястребы` | initial stress marker | lexical stress | YES, `pronunciations.toml` | safe lexicon entry; preserve exact known forms | other inflections not in evidence | confirmed |
| `big-part`: `большая часть` | `больш+ая часть` | phrase stress | YES, `pronunciations.toml` | phrase resolver | `большая` outside this phrase | confirmed |
| `podast-ruki`: `подаст руки` | `подаст рук+и` | phrase stress / inflection | YES, `pronunciations.toml` | phrase resolver | `подаст` in other government/meaning | confirmed |
| `start-yusupova`: `начала Юсупова` | `начал+а Юсупова` | homograph / syntax-government | YES, narrow TOML phrases | contextual phrase resolver | `начала` as verb “began”; other names | confirmed |
| `start-vika`: `начала Вика` | `начал+а Вика` | homograph / syntax-government | YES, narrow TOML phrase | contextual phrase resolver | `начала` outside attribution | confirmed |
| `his-words`: `в его словах` | `в его слов+ах` | phrase stress | YES, TOML | phrase resolver | other `словах` contexts | confirmed |
| `k-tomu`: `к тому`, `к тому, чтобы` | `к том+у` | syntax-government | YES, TOML | phrase resolver | `тому` in unrelated constructions | confirmed |
| `maloe`: `малое дофига` | `м+алое дофига` | phrase stress | YES, TOML | phrase resolver | `малое` outside phrase | confirmed |
| `popadalo`: `под это определение не попадало` | `... не попад+ало` | homograph / syntax | YES, TOML | contextual resolver | `яблоко попадало с дерева` | confirmed |
| `boli`: `испугался он явно не боли` | `... не б+оли` | homograph / syntax | YES, TOML | contextual resolver | `Боли сильнее!`, imperative `боли` | confirmed |
| `vody`: `глотнув/глотнуть/вкусной воды` | `вод+ы` | syntax-government | YES, TOML | contextual resolver | `минеральные воды`, plural meaning | confirmed |
| `zamorozi`: `заморозки` | `замор+озки` | lexical stress | YES, TOML | safe only for evidenced noun usage | verb/other lexical readings if later found | confirmed |
| `tushe`: `туше` | `туш+е` | lexical stress | YES, TOML | safe lexicon entry | unrelated homographs if discovered | confirmed |
| `vtoroy`: `второй` and declensions | `втор+ой`, corresponding forms | lexical stress / inflection | YES, TOML | safe lexicon paradigm | other words sharing prefixes | confirmed |
| `maksim`: `Максим` and forms | `Макс+им`, corresponding forms | proper name | YES, TOML | project lexicon entry | common-word/other-name collisions | confirmed |
| `valerych`: `Валерыч` and forms | `Вал+ерыч`, corresponding forms | proper name | YES, TOML | project lexicon entry | other patronymic/name spellings | confirmed |
| `odin-v-odin`: `один в один` | `один в од+ин` | phrase stress | YES, `tts_silero.py` | phrase resolver | `Бог Один ...`; single `один` | confirmed |
| `vse-vsyo`: `все/всё` idioms and plural subjects | `всё ...` or protected `вс+е` | homograph / phrase stress | YES, `tts_silero.py` | context resolver before segmentation | plural `все`; explicit `всё`; `Все же события...` | confirmed, known incomplete |
| `censor-mask`: `**`, `*-*`, internal `сло**во` | `пик` or `…` according to position | censor | YES, `prepare_silero_text` | common compiler transform with change records | ordinary asterisks; partial masks | confirmed |
| `identifier-zero`: `80-03`, `80−03` | `80 дефис ноль три` | number/time identifier | YES, `prepare_silero_text` | common deterministic transform | `80-13`; embedded digits | confirmed |
| `clock`: `08.30`, contextual `в 3.14` control | `8 30` / `3.14` unchanged without cue | number/time identifier | YES, `prepare_silero_text` | common contextual transform | decimal `3.14`; non-time punctuation | confirmed |
| `interrobang`: `⁈` | `?!` | punctuation | YES, `prepare_silero_text` and splitter | common punctuation normalization | dialogue `Что⁈ — спросил он` boundary | confirmed |
| `abbrev-hardening`: `н. э.`, `д. н. э.` | literal-dot Silero patterns only | punctuation / backend safety | YES, `harden_silero_ru_preprocessing` | isolated Silero backend hook | `на этот`, `на эшафот` | confirmed |
| `FB2-title`: `<title><p>...` plus repeated first body paragraph | one structural heading | structural FB2 | YES, `fb2_parser.py` | parser-owned source structure, compiler consumes it | later repeated paragraph preserved | confirmed |
| `FB2-structure`: title/body and paragraph identity | no flattening or paragraph crossing | structural FB2 | YES, parser + splitter | structured compiler units and stable IDs | adjacent paragraphs; title/body boundary | confirmed |
| `malformed-heading`: `.Глава 16` duplicate | deduplicate only leading structural duplicate | structural FB2 | YES, parser normalization | parser/compiler structural rule | later `.Глава 16` remains | confirmed |
| `punct-only`: `— …`, `?!`, `⁈` | no TTS segment | segmentation | YES, splitter | splitter invariant | `— ******!` retains speech mask | confirmed |
| `dialogue-boundary`: `— Могу ли я?.. — спросил Павел.` | one dialogue segment | segmentation / punctuation | YES, splitter | preserve structured segment boundaries | clear next sentence after `?..` | confirmed |
| `spacy-cache`: missing `ru_core_news_sm` | one cached failed load | segmentation | YES, splitter | unchanged splitter service behavior | two paragraphs trigger one load attempt | confirmed |
| `pause-metadata`: segment boundary/edge metadata | pause policy sees source boundary and measured edges | segmentation / audio contract | YES, pipeline + diagnostics + pause policy | compiler emits segment IDs/metadata; audio layer unchanged | no global `0.3` stacking | confirmed |
| `pause-policy`: target minus existing edge silence | `max(0, target - trailing - leading)` | expressive prosody / audio | YES, `pause_policy.py` | protected audio layer, not compiler | existing silence and chapter target | confirmed |
| `ffmpeg-189`: 189 segments | integer sample padding and `end_sample` | audio integration | YES, `audio_assembler.py` | protected audio layer | scientific notation duration regression | confirmed |
| `ob-rechyonno`: `обречённо` | `обречённо` with stress on `ё` | lexical stress | NO, journal confirmed listening case | compiler lexicon entry; safe lexical form | unrelated `обречённый` forms | confirmed |
| `two-and-half-hours`: `два с половиной часа` | `два с половиной час+а` | inflection / phrase stress | NO | contextual phrase resolver | other `часа` readings | confirmed |
| `nabralos`: `набра́лось` | `набрал+ось` | lexical stress | NO | narrow lexical/context rule | other `набралось` contexts if meaning differs | confirmed |
| `ne-bylo`: `никого не было`, `вопросов не было` | `никого н+е было`, `вопросов н+е было` | phrase stress / syntax | NO | negative-construction resolver | cases with contrastive stress on `было` | confirmed |
| `potom`: `пОтом` vs `потОм` | context-dependent `пот+ом` only where “then” | homograph / phrase stress | NO | contextual resolver, never global replacement | `холодным потом`, `хера́ себе`-style unrelated phrase | confirmed observation, scope narrow |
| `glaza`: `открывать глаза`, `поднял глаза` | `... глаз+а` | inflection / syntax-government | PARTIAL, existing handoff/TOML may contain only selected forms | contextual resolver | `глаза` plural subject/object contexts | confirmed |
| `sreda`: day-of-week `среду` | `ср+еду` | homograph / syntax | NO | context resolver | `среду` as environment/medium remains unchanged | confirmed |
| `zamok`: lock `замок` | `зам+ок` | homograph / semantic context | NO | cue-based contextual resolver | castle `з+амок`, `старый замок` | confirmed |
| `statiu`: `с королевской статью` | `с королевской стАтью` | inflection / syntax-government | NO | phrase resolver | other `статью` uses | confirmed |
| `ne-s-chem`: `не с чем` | `н+е с чем` | phrase stress / syntax | NO | phrase resolver | do not globally stress `чем` | confirmed |
| `vysoty`: `Я высоты боюсь` | `Я высот+ы боюсь` | syntax-government | NO | contextual resolver | `высОты` plural/genitive alternatives | confirmed |
| `strelku`: `пока стрелку не надоест` | `пока стрелк+у не надоест` | inflection / syntax-government | NO | contextual resolver | `стрЕлку` as arrow/person object | confirmed |
| `hlopok`: `хлопок вышибного заряда` | `хлоп+ок` | homograph / semantic context | NO | semantic cue resolver | cotton/plant `хл+опок` contexts | confirmed |
| `steny`: `в сторону стены` | `в сторону стен+ы` | syntax-government | NO | contextual resolver | plural `стЕны` contexts | confirmed |
| `napadavshih`: `четверо нападавших` | `четверо напад+авших` | inflection / lexical stress | NO | lexical paradigm or narrow resolver | other forms/meanings | confirmed |
| `rodov`: `представители великих родов` | `великих род+ов` | homograph / semantic context | NO | semantic cue resolver | `р+оды` = childbirth | confirmed |
| `litsa`: `красноте лица` | `красноте лиц+а` | syntax-government | NO | contextual resolver | plural `л+ица` | confirmed |
| `galitsyn`: `Галицын`, case forms | `Гал+ицын`, forms with same stem stress | proper name | NO | explicit book/project lexicon profile only | universal surname pronunciation must remain untouched | confirmed, project-specific |
| `borisovich`: `Борисович` | `Бор+исович` if existing class requires it | proper name / patronymic | PARTIAL/verify existing implementation first | existing patronymic-class hook, no blanket suffix regex | unrelated patronymics and other stress | observed/verification required |
| `kher`: `какого хера`, `хера себе` | no global rewrite; phrase-specific only | phrase stress | NO | experimental/context resolver with negative controls | `хер+а себе`; Gramota permits variants | unresolved as universal rule |
| `long-vowels`: `о-о-о`, `ааа`, `не-е-ет` | explicit expressive runs -> exactly 3 contiguous vowels; ordinary triples unchanged | expressive prosody | YES, `tts_preprocessor.py` | human-selected v3 transform; plain runs require 4+ copies | normal repeated letters; punctuation; initial standalone `О` model artifact | confirmed workaround / model limitation remains |
| `acronym`: `СВУ`, `СИБ` | explicit `spell_letters` vs `lexicalized_word` | acronym | NO | lexicon resolver with unknown/log-only fallback | never `ALL_CAPS => letters` | experimental / unresolved |

## Consolidation decisions

1. Rules currently embedded in `tts_silero.py` move behind a deterministic compiler
   API. Thin compatibility imports remain for existing callers/tests.
2. Context rules run on a structured chapter paragraph before final segmentation;
   no paragraph is flattened to gain context.
3. Project-name rules require an explicit profile/override; `Галицын` is not made a
   universal surname rule.
4. Long-vowel handling uses the human-selected v3 best-effort transform; acronym
   handling remains architecture-only and unresolved.
5. Pause policy, edge metadata, FFmpeg sample padding, and diagnostics remain
   downstream contracts. The compiler records source/normalized/segment identity
   but does not alter audio timing semantics.

## Feature-branch implementation delta

The table's `implemented now` column intentionally records the pre-branch
baseline so the migration is auditable. On this branch, the following are now
implemented in `src/core/tts_preprocessor.py` and/or pipeline integration:

- existing dictionary, `все/всё`, censor, identifier, clock, interrobang, and
  safe-abbreviation behavior is available through the compiler compatibility API;
- `обреченно`, `два с половиной часа`, `набралось`, negative `не было`, temporal
  `а/и потом`, eyes, day-of-week `среду`, lock cues, `статью`, `не с чем`,
  `высоты`, `стрелку`, `хлопок`, `стены`, `нападавших`, `родов`, and `лица` have
  deterministic narrow rules with tests and controls;
- `Галицын` is implemented only when the explicit profile resolves to the known
  `Гимн шута`/`book9` project profile;
- acronym handling remains intentionally unresolved for production; long-vowel
  normalization is now production v3 with the documented model limitation;
- `какого хера` remains intentionally unresolved as a universal rule because the
  journal records accepted normative variants and requires phrase-specific proof;
- `Борисович` remains a verification/debt item until an existing patronymic class
  or sufficiently bounded rule is identified.
