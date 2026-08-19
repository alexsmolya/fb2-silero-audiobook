# Book 09/10 corpus context audit

Generated from local FB2 with the current parser, TtsPreprocessor and SentenceSplitter. MP3 times are approximate paragraph-ratio localization only; they are not alignment or stress evidence.

Target occurrence rows: 1072

## Expressive-vowel production dry-run

Human A/B listening selected **v3: exactly three contiguous copies** of the
explicitly stretched vowel. Across the 113 expressive audit rows, 110 were
transformed and 3 were intentionally skipped: `эээ`, `Эээ`, and `Фамилиии`
in book 9. These are ordinary triple/lexical spellings without explicit
expressive notation. Suspicious cases: 0; all 113 rows passed lexical
character-preservation checks.

The standalone initial `О` in book 10 chapter 4 paragraph 79 remains outside
the transform. Its observed realization as `А` is a separate Silero
`MODEL_LIMITATION`, not a preprocessing target.

## Segmentation metrics
### Book 9
- fb2: /home/alex/Загрузки/AudioBook/книги  9,10 на анализ/09 Гимн шута - 09.fb2
- mp3: /home/alex/Загрузки/AudioBook/книги  9,10 на анализ/09 Гимн шута - 09.mp3
- chapters: 23
- source_paragraphs: 2819
- normalized_paragraphs: 2819
- segments: 6394
- paragraph_crossings: 0
- title_body_accidental_merges: 0
- title_body_boundary_cases: 23
- punctuation_only_segments: 0
- empty_segments: 0
- suspicious_very_short_segments: 301
- suspicious_very_long_segments: 0
- dialogue_boundary_cases: 14
- question_ellipsis_interrobang_samples: 1
- stable_segment_ordering: True
- censor_mask_survival: True
- mp3_duration_seconds: 20903.454014
- sample segments:
  - `chapter_start` p0: Глава первая
  - `title_body` p2: — Просыпайся!
  - `paragraph` p3: — Ну еще пять минуточек!
  - `paragraph` p4: Однако уснуть вновь не получилось.
  - `paragraph` p5: — Дааай!
  - `paragraph` p6: Та, обозначив ехидную улыбку, отступила на пару шагов назад, демонстрируя молодому человеку уже перезаряженный согревающий амулет.
  - `paragraph` p7: — Цып-цып-цып-цып-цыпа!.. — протянула боевик, еще больше разрывая дистанцию.
  - `paragraph` p8: — Да встаю, встаю, — молодой человек, расстегивая спальник.
  - `paragraph` p9: Морозец тут же иголками впился в кожу, заставив поежиться.
  - `paragraph` p10: — Держи!
  - `paragraph` p11: Естественно, тот без труда поймал подарок и тут же повесил себе на шею.
  - `paragraph` p12: — На пару часов хватит, — сообщила культуристка.
  - `paragraph` p13: С этими словами Валентина покружилась на месте, позволяя коллеге оценить свой новый «лук» полностью.
  - `paragraph` p14: — Вещь, — согласился молодой человек, растирая лицо снегом.
  - `paragraph` p15: Тишь застыла.
  - `paragraph` p16: — Сотни тысяч рублей, самые современные технологии, готовность практически к любому театру боевых действий за тридцать минут… а простейший мятный леденец не предусмотрели!
### Book 10
- fb2: /home/alex/Загрузки/AudioBook/книги  9,10 на анализ/10 Гимн шута - 10.fb2
- mp3: /home/alex/Загрузки/AudioBook/книги  9,10 на анализ/10 Гимн шута - 10.mp3
- chapters: 28
- source_paragraphs: 2872
- normalized_paragraphs: 2872
- segments: 6387
- paragraph_crossings: 0
- title_body_accidental_merges: 0
- title_body_boundary_cases: 28
- punctuation_only_segments: 0
- empty_segments: 0
- suspicious_very_short_segments: 309
- suspicious_very_long_segments: 0
- dialogue_boundary_cases: 14
- question_ellipsis_interrobang_samples: 0
- stable_segment_ordering: True
- censor_mask_survival: True
- mp3_duration_seconds: 20831.829388
- sample segments:
  - `chapter_start` p0: Глава первая Пролог
  - `title_body` p3: Глава первая.
  - `paragraph` p4: Небо над столицей стремительно темнело.
  - `paragraph` p5: За спиной наблюдающего за вечерним небом мужчины с мягким шорохом разошлись в сторону автоматические створки двери.
  - `paragraph` p6: — Проходи, Игнат, — предложил Лев Дем+идович.
  - `paragraph` p7: Будущий глава упрашиваться себя не заставил.
  - `paragraph` p8: — Что скажешь, сын?
  - `paragraph` p9: — П…ц, — коротко охарактеризовал положение Юсупов-младший, сжимая в руках оборудованный засекречивающей аппаратурой связи планшет.
  - `paragraph` p10: Этот вечер он провел в знакомстве с «трудами» Волконского, чьи люди вот уже несколько месяцев фиксировали каждый шаг их противников.
  - `paragraph` p11: — Что самое главное ты можешь отметить в полученной информации?
  - `paragraph` p12: — Эти с…ки заигрались!
  - `paragraph` p13: — Сдержанней, — потребовал отец.
  - `paragraph` p14: Совсем скоро его сыну предстояло занять Трон.
  - `paragraph` p15: — Некоторые родичи явно вышли за приделы клановой этики Юсуповых, — ровно поправился Игнат, бросив короткий, но выразительный взгляд на отца.
  - `paragraph` p16: — Уже лучше, — согласился тот.
  - `paragraph` p17: Будущий Глава потер виски, почувствовав первые признаки приближающей головной боли.

## Target contexts
### Book 9 / ch-0001-p-0004 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А за новой все равно придется выбираться из уютного «кокона».
- current normalized: А за новой всё равно придется выбираться из уютного «кокона».
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: 29.66 s; clip: `/tmp/book09-10-forensic/clips/book09_001__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0001-p-0005 / `Да-а-а-ай`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Да-а-а-ай!
- current normalized: — Дааай!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: 37.08 s; clip: `/tmp/book09-10-forensic/clips/book09_001_expressive_elongation.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0001-p-0018 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: От глайдера Волконского (по легенде, СИБ прибыли только ночью, а до того времени в местной «зеленке» исключительно гвардейцы клановца «партизанили») к дому Николая Александровича, которому врачи помочь просто не успели.
- current normalized: От глайдера Волконского (по легенде, СИБ прибыли только ночью, а до того времени в местной «зеленке» исключительно гвардейцы клановца «партизанили») к дому Николая Александровича, которому врачи помочь просто не успели.
- current rule: `none`
- approximate MP3: 133.47 s; clip: `/tmp/book09-10-forensic/clips/book09_001__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0001-p-0038 / `Спа-а-а-асибо`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Спа-а-а-асибо!
- current normalized: — Спааасибо!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: 281.78 s; clip: `/tmp/book09-10-forensic/clips/book09_001_expressive_elongation.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0001-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А Тишь еще и покрутиться на месте изволила, чтобы уж точно все присутствующие оценили ее величие и неотразимость!
- current normalized: А Тишь еще и покрутиться на месте изволила, чтобы уж точно все присутствующие оценили ее величие и неотразимость!
- current rule: `lexicon.project`
- approximate MP3: 289.19 s; clip: `/tmp/book09-10-forensic/clips/book09_001__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0001-p-0041 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Теперь я видел все…
- current normalized: — Теперь я видел все…
- current rule: `none`
- approximate MP3: 304.02 s; clip: `/tmp/book09-10-forensic/clips/book09_001__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0001-p-0043 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Павел Анатольевич, — уже официально объявил собравшийся помощник воеводы, все еще не отводя от валькирии пораженного взгляда.
- current normalized: — Павел Анатольевич, — уже официально объявил собравшийся помощник воеводы, всё еще не отводя от валькирии пораженного взгляда.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: 318.85 s; clip: `/tmp/book09-10-forensic/clips/book09_001__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0009 / `стеночки`
- class: стены; verdict: **OK**
- FB2 sentence: — раздраженно огрызнулась девушка, заставив выстроившихся вдоль стеночки поваров заметно побледнеть.
- current normalized: — раздраженно огрызнулась девушка, заставив выстроившихся вдоль стеночки поваров заметно побледнеть.
- current rule: `silero.preprocessing`
- approximate MP3: 66.74 s; clip: `/tmp/book09-10-forensic/clips/book09_002__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0029 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Обычно все было великолепно приготовлено, тщательно сбалансировано и…
- current normalized: Обычно все было великолепно приготовлено, тщательно сбалансировано и…
- current rule: `lexicon.project`
- approximate MP3: 215.04 s; clip: `/tmp/book09-10-forensic/clips/book09_002__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0035 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Стало быть, нормально все.
- current normalized: Стало быть, нормально все.
- current rule: `none`
- approximate MP3: 259.53 s; clip: `/tmp/book09-10-forensic/clips/book09_002__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В этот раз она все-таки воспользовалась куда более подходящим для его отбивки инструментом, чем собственные кулаки.
- current normalized: В этот раз она всё-таки воспользовалась куда более подходящим для его отбивки инструментом, чем собственные кулаки.
- current rule: `silero.preprocessing`
- approximate MP3: 281.78 s; clip: `/tmp/book09-10-forensic/clips/book09_002__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0048 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Простая ремарка заставила задуматься все руководство клана Волконских.
- current normalized: Простая ремарка заставила задуматься все руководство клана Волконских.
- current rule: `none`
- approximate MP3: 355.93 s; clip: `/tmp/book09-10-forensic/clips/book09_002__.mp3`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0052 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Первым в глаза бросалось сообщение: «Светка, смотри какой костюмчик!
- current normalized: Первым в глаза бросалось сообщение: «Светка, смотри какой костюмчик!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0053 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Убедившись, что все ознакомились с посланием, Волконская открыла прикрепленное к нему фото.
- current normalized: Убедившись, что вс+е ознакомились с посланием, Волконская открыла прикрепленное к нему фото.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0054 / `Но-о-ормально`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Но-о-ормально, — оценил Валерыч.
- current normalized: — Нооормально, — оценил Вал+ерыч.
- current rule: `lexicon.project, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0066 / `глазам`
- class: глаза; verdict: **OK**
- FB2 sentence: Судя по покрасневшим глазам и чуть рассеянному взгляду ночь у «принцессы» выдалась не самая легкая.
- current normalized: Судя по покрасневшим глазам и чуть рассеянному взгляду ночь у «принцессы» выдалась не самая легкая.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0073 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А потому, рано или поздно, за все «подарки» те же Юсуповы спросят.
- current normalized: А потому, рано или поздно, за все «подарки» те же Юсуповы спросят.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0082 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Оказалось, поддерживать «картинку» куда проще, чем контролировать все сорок три лицевые мышцы.
- current normalized: Оказалось, поддерживать «картинку» куда проще, чем контролировать все сорок три лицевые мышцы.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0095 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все же события последних суток…
- current normalized: Но всё же события последних суток…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0098 / `че-е-е-е-ерт`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Чет че-е-е-е-ерт, — протянул он.
- current normalized: — Чет чееерт, — протянул он.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0101 / `ка-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Вот ка-а-а-ак⁈
- current normalized: — Вот кааак?!
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0108 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: — Понимаю, — кивнул воевода, так и не стерев с лица легкой улыбки, что, если честно, довольно сильно раздражало клановца.
- current normalized: — Понимаю, — кивнул воевода, так и не стерев с лица легкой улыбки, что, если честно, довольно сильно раздражало клановца.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0116 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: Наградой за попадание ему стали круглые глазки «принцессы», в которых теперь плескалась толика страха.
- current normalized: Наградой за попадание ему стали круглые глазки «принцессы», в которых теперь плескалась толика страха.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0145 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Значит, на этот раз все всерьез.
- current normalized: — Значит, на этот раз всё всерьез.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0148 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: Однако дальнейшее сопротивление приведет к тому, что он в глазах руководства пересечет очень хреновую черту.
- current normalized: Однако дальнейшее сопротивление приведет к тому, что он в глазах руководства пересечет очень хреновую черту.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0002-p-0151 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Лишь через несколько минут, получив дополнительное подтверждение от все того же абонента, он негромко хмыкнул:
- current normalized: Лишь через несколько минут, получив дополнительное подтверждение от всё того же абонента, он негромко хмыкнул:
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Как все…
- current normalized: — Как все…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0016 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Нет, Павел был совершенно точно уверен, что все закончится хорошо.
- current normalized: Нет, Павел был совершенно точно уверен, что все закончится хорошо.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0021 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все информационное сопровождение взял на себя клан.
- current normalized: Все информационное сопровождение взял на себя клан.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0034 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Клановец же, напротив, все сильнее заинтересовался беседой.
- current normalized: Клановец же, напротив, всё сильнее заинтересовался беседой.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0059 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Он все также провожал гордым взглядом сына.
- current normalized: Он все также провожал гордым взглядом сына.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0062 / `Глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаз не отвел от лица собеседника.
- current normalized: Глаз не отвел от лица собеседника.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0062 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Глаз не отвел от лица собеседника.
- current normalized: Глаз не отвел от лица собеседника.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0067 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все с приставкой «спец-»: спецподбор, спецподготовка, спецкомплектование.
- current normalized: И все с приставкой «спец-»: спецподбор, спецподготовка, спецкомплектование.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0070 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки, готовить операцию глава разведупра помогал лично.
- current normalized: Всё-таки, готовить операцию глава разведупра помогал лично.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0071 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Тем неожиданнее было превращение недавнего союзника в жестокого конкурента, моментально изолировавшего практически все контакты и средства связи Николая Александровича.
- current normalized: Тем неожиданнее было превращение недавнего союзника в жестокого конкурента, моментально изолировавшего практически все контакты и средства связи Николая Александровича.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0081 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Родственник все же…
- current normalized: Родственник всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0083 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Родич, все ж таки…
- current normalized: Родич, всё ж таки…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0092 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Мы можем договориться, — без всяких раздумий заверил Константин Ильич, в моменте готовый пообещать вообще все что угодно.
- current normalized: — Мы можем договориться, — без всяких раздумий заверил Константин Ильич, в моменте готовый пообещать вообще все что угодно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0100 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: С этого момента все пошло наперекосяк.
- current normalized: С этого момента все пошло наперекосяк.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0108 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Наверняка все разом так удобно «вышли из строя».
- current normalized: Наверняка все разом так удобно «вышли из строя».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0108 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: Тот оперся на стену и молча наблюдал за уходящим родичем.
- current normalized: Тот оперся на стену и молча наблюдал за уходящим родичем.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0124 / `Спаси-и-и-и-и-ибо`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Спаси-и-и-и-и-ибо!
- current normalized: — Спасииибо!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0127 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все самое интересное было скрыто спиной Леночки.
- current normalized: Всё самое интересное было скрыто спиной Леночки.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0127 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако фантазия без труда «дорисовывала» все необходимое.
- current normalized: Однако фантазия без труда «дорисовывала» всё необходимое.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0131 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — А еще у нас есть для тебя много-много игрушек, — мечтательно закатила глаза Леночка и походкой манекенщицы отправилась к стене, откуда приволокла довольно увесистую сумку.
- current normalized: — А еще у нас есть для тебя много-много игрушек, — мечтательно закатила глаза Леночка и походкой манекенщицы отправилась к стене, откуда приволокла довольно увесистую сумку.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0003-p-0131 / `стене`
- class: стены; verdict: **OK**
- FB2 sentence: — А еще у нас есть для тебя много-много игрушек, — мечтательно закатила глаза Леночка и походкой манекенщицы отправилась к стене, откуда приволокла довольно увесистую сумку.
- current normalized: — А еще у нас есть для тебя много-много игрушек, — мечтательно закатила глаза Леночка и походкой манекенщицы отправилась к стене, откуда приволокла довольно увесистую сумку.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Зато повеселились все знатно.
- current normalized: Зато повеселились все знатно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0005 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — Не сплю, — согласился тот, открывая глаза.
- current normalized: — Не сплю, — согласился тот, открывая глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Волконский с известным сожалением проводил стройную фигурку, с каждой секундой все больше скрывавшуюся под одеждой, взглядом.
- current normalized: Волконский с известным сожалением проводил стройную фигурку, с каждой секундой всё больше скрывавшуюся под одеждой, взглядом.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0010 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Павел в ответ только глаза округлил.
- current normalized: Павел в ответ только глаза округлил.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0011 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Если противник УЖЕ прошел охранные контуры из дежурных спецов СИБ и гвардейцев, обманув хитровымудренную электронику и артефакторные цепи, то все настолько плохо, что никакой пистолет уже не поможет.
- current normalized: Если противник УЖЕ прошел охранные контуры из дежурных спецов СИБ и гвардейцев, обманув хитровымудренную электронику и артефакторные цепи, то все настолько плохо, что никакой пистолет уже не поможет.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0011 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Если противник УЖЕ прошел охранные контуры из дежурных спецов СИБ и гвардейцев, обманув хитровымудренную электронику и артефакторные цепи, то все настолько плохо, что никакой пистолет уже не поможет.
- current normalized: Если противник УЖЕ прошел охранные контуры из дежурных спецов СИБ и гвардейцев, обманув хитровымудренную электронику и артефакторные цепи, то все настолько плохо, что никакой пистолет уже не поможет.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0015 / `Э-э-э`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Э-э-э-й!
- current normalized: — ЭЭЭ-й!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0017 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Стоит только отбросить слово «невозможно» из уравнения и все тут же встает на свои места.
- current normalized: Стоит только отбросить слово «невозможно» из уравнения и вс+е тут же встает на свои места.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0033 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: утаскивая на глазах ошарашенного Павла бутерброд с тарелки…
- current normalized: утаскивая на глазах ошарашенного Павла бутерброд с тарелки…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0036 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: При этом помощник Павла столь жалобно закатил глаза, что рассмеялись вообще все.
- current normalized: При этом помощник Павла столь жалобно закатил глаза, что рассмеялись вообще все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0036 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: При этом помощник Павла столь жалобно закатил глаза, что рассмеялись вообще все.
- current normalized: При этом помощник Павла столь жалобно закатил глаза, что рассмеялись вообще все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0039 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все им кому-то чего-то доказывать нужно!
- current normalized: Все им кому-то чего-то доказывать нужно!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: От этого выигрывали буквально все!
- current normalized: От этого выигрывали буквально все!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0041 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Ну, почти все!
- current normalized: «Ну, почти все!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0049 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: — Могу добить, — предложила она, и тут же, в ответ на осуждение в глазах присутствующих, невинно пожала плечами.
- current normalized: — Могу добить, — предложила она, и тут же, в ответ на осуждение в глазах присутствующих, невинно пожала плечами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0064 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Та, конечно, изо всех сил пыталась делать вид, что все нормально, но подобное «обоснование» для нее пока было слишком.
- current normalized: Та, конечно, изо всех сил пыталась делать вид, что все нормально, но подобное «обоснование» для нее пока было слишком.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0068 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Выдав пару конструкций в адрес гаджета, молодой человек все-таки активировал модуль ЗАС.
- current normalized: Выдав пару конструкций в адрес гаджета, молодой человек всё-таки активировал модуль ЗАС.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0074 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Теперь на кухне примолкли вообще все.
- current normalized: Теперь на кухне примолкли вообще все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0079 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все в порядк?..
- current normalized: — Все в порядк?..
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0080 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: И лишь потом поднес гаджет к уху.
- current normalized: И лишь потом поднес гаджет к уху.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0084 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако все же ограничился коротким сообщением.
- current normalized: Однако всё же ограничился коротким сообщением.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0004-p-0084 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Несколько секунд Волконский размышлял, не подключить ли спецов СИБ.
- current normalized: Несколько секунд Волконский размышлял, не подключить ли спецов СИБ.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0005 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: ), если развести в стороны полы пиджака девушки, то водолазка под ним окажется столь тонкой и обтягивающей, что все анатомические подробности угадывались также явно, как если бы ее совсем не было!
- current normalized: ), если развести в стороны полы пиджака девушки, то водолазка под ним окажется столь тонкой и обтягивающей, что все анатомические подробности угадывались также явно, как если бы ее совсем не было!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0010 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Так что СИБ я бы подключать не хотел.
- current normalized: Так что СИБ я бы подключать не хотел.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0013 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все равно еще Катерину дожидаться.
- current normalized: Всё равно еще Катерину дожидаться.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0020 / `Что-о-о-о`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Что-о-о-о?..
- current normalized: — Чтооо?..
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0029 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: — оценил он, окинув взглядом стены.
- current normalized: — оценил он, окинув взглядом стены.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0036 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Собеседник не удержал лица.
- current normalized: Собеседник не удержал лица.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0051 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Андрей непонимающе округлил глаза.
- current normalized: Андрей непонимающе округлил глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0056 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки сильно вряд ли, что от него потребуют заняться этим именно сейчас.
- current normalized: Всё-таки сильно вряд ли, что от него потребуют заняться этим именно сейчас.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0073 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Тогда на этом у меня все, — коротко кивнул Андрей.
- current normalized: — Тогда на этом у меня все, — коротко кивнул Андрей.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0005-p-0079 / `Во-о-о-от`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Во-о-о-от…
- current normalized: — Вооот…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0003 / `стрелковка`
- class: стрелку; verdict: **OK**
- FB2 sentence: Мобильное ПВО, системы радиоэлектронной борьбы и разведки, серьезная «стрелковка» с глушителями и прочими приблудами, к частному обороту на территории империи запрещенное как класс.
- current normalized: Мобильное ПВО, системы радиоэлектронной борьбы и разведки, серьезная «стрелковка» с глушителями и прочими приблудами, к частному обороту на территории империи запрещенное как класс.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0003 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: Рвал документы, а метнул тяжелое пресс-папье в стену в тщетной попытке восстановить хотя бы часть душевного равновесия.
- current normalized: Рвал документы, а метнул тяжелое пресс-папье в стену в тщетной попытке восстановить хотя бы часть душевного равновесия.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0021 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: На Никиту Ивановича впечатления не произвели ни резкий тон, ни краснота начальственного лица, ни дерганная моторика господина.
- current normalized: На Никиту Ивановича впечатления не произвели ни резкий тон, ни краснота начальственного лица, ни дерганная моторика господина.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0028 / `стен`
- class: стены; verdict: **OK**
- FB2 sentence: Почти минуту хозяин кабинета тяжело дышал, разглядывая облака сквозь панорамное окно, занимавшее одну из стен полностью, сверху вниз.
- current normalized: Почти минуту хозяин кабинета тяжело дышал, разглядывая облака сквозь панорамное окно, занимавшее одну из стен полностью, сверху вниз.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ему в целом было все равно, зачем именно его господину понадобилось ввязываться в «маленькую победоносную войну»…
- current normalized: Ему в целом было всё равно, зачем именно его господину понадобилось ввязываться в «маленькую победоносную войну»…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0039 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все это исчезло?
- current normalized: Всё это исчезло?
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0058 / `стене`
- class: стены; verdict: **OK**
- FB2 sentence: Разведчик вскочил с кресла и метнулся к противоположной стене кабинета.
- current normalized: Разведчик вскочил с кресла и метнулся к противоположной стене кабинета.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0061 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Просто потому, что отдать под «пресс» СИБ человека с таким уровнем информирования — смерти подобно.
- current normalized: Просто потому, что отдать под «пресс» СИБ человека с таким уровнем информирования — смерти подобно.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0062 / `ма-а-а-аленькая`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Была всего лишь одна ма-а-а-аленькая проблемка.
- current normalized: Была всего лишь одна маааленькая проблемка.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0079 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Со стороны могло показаться, что седой, но все еще крепкий мужчина, которого язык не повернется назвать стариком, вот уже пару часов просидел на раскладном туристическом стульчике почти без движения.
- current normalized: Со стороны могло показаться, что седой, но всё еще крепкий мужчина, которого язык не повернется назвать стариком, вот уже пару часов просидел на раскладном туристическом стульчике почти без движения.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0079 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Лишь умные голубые глаза внимательно следили за поплавком, по привычке не упуская цель из виду ни на миг.
- current normalized: Лишь умные голубые глаза внимательно следили за поплавком, по привычке не упуская цель из виду ни на миг.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0081 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — буркнул Семеныч, все также наблюдая за поплавком.
- current normalized: — буркнул Семеныч, все также наблюдая за поплавком.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0006-p-0082 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И рыбаку на какой-то миг захотелось поверить, что его собеседник все поймет и повесит трубку.
- current normalized: И рыбаку на какой-то миг захотелось поверить, что его собеседник все поймет и повесит трубку.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0013 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Клановец кивнул, принимая объяснение, но все-таки с легкой опаской покосился на исполняющую довольно резкие, но вполне четкие маневры между полосами девушку.
- current normalized: Клановец кивнул, принимая объяснение, но всё-таки с легкой опаской покосился на исполняющую довольно резкие, но вполне четкие маневры между полосами девушку.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0050 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Катерина сделала небольшую паузу, но все же кивнула.
- current normalized: Катерина сделала небольшую паузу, но всё же кивнула.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0052 / `Та-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-ак, — вздохнул негромко Волконский.
- current normalized: — Тааак, — вздохнул негромко Волконский.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0055 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Очень ему не нравилось это ощущение, когда все ведут себя так, будто бы знают нечто совершенно недоступное его пониманию.
- current normalized: Очень ему не нравилось это ощущение, когда вс+е ведут себя так, будто бы знают нечто совершенно недоступное его пониманию.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0057 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: своей девушки, сколько ей предложений поступает о работе, — покачала головой блондиночка, но под прицелом внимательных глаз, все-таки начала объяснять.
- current normalized: своей девушки, сколько ей предложений поступает о работе, — покачала головой блондиночка, но под прицелом внимательных глаз, всё-таки начала объяснять.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0057 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: своей девушки, сколько ей предложений поступает о работе, — покачала головой блондиночка, но под прицелом внимательных глаз, все-таки начала объяснять.
- current normalized: своей девушки, сколько ей предложений поступает о работе, — покачала головой блондиночка, но под прицелом внимательных глаз, всё-таки начала объяснять.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0058 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все они на спецучете.
- current normalized: И все они на спецучете.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0068 / `Та-а-а-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-а-а-ак, — вздохнул клановец.
- current normalized: — Тааак, — вздохнул клановец.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0072 / `Ка-а-а-атя`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ка-а-а-атя!
- current normalized: — Кааатя!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0078 / `Родов`
- class: родов; verdict: **OK**
- FB2 sentence: Почему же тогда за Лену не заступились представители Родов и кланов?
- current normalized: Почему же тогда за Лену не заступились представители Родов и кланов?
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0080 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: — Знаешь, — в глазах блондиночки вспыхнул лукавый огонек.
- current normalized: — Знаешь, — в глазах блондиночки вспыхнул лукавый огонек.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0104 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все цели спецы «закрыли», оставив после себя множество трупов, но никаких свидетелей и зацепок.
- current normalized: Вс+е цели спецы «закрыли», оставив после себя множество трупов, но никаких свидетелей и зацепок.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0007-p-0105 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Сотрудничество с Юсуповыми стоит мне лично все дороже и дороже.
- current normalized: — Сотрудничество с Юсуповыми стоит мне лично всё дороже и дороже.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Они все-таки закончили «разговор» на заднем сидении «Империала».
- current normalized: Они всё-таки закончили «разговор» на заднем сидении «Империала».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0004 / `Чего-о-о`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Чего-о-о⁈
- current normalized: — Чегооо?!
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0005 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: На его взгляд, все происходящее оценки выше «Ну-у-у-у…
- current normalized: На его взгляд, все происходящее оценки выше «Нууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0005 / `Ну-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: На его взгляд, все происходящее оценки выше «Ну-у-у-у…
- current normalized: На его взгляд, все происходящее оценки выше «Нууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0006 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: — Да я про кофе, — усмехнулась Катерина, блеснув в темноте глазками бесстыжими.
- current normalized: — Да я про кофе, — усмехнулась Катерина, блеснув в темноте глазками бесстыжими.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0008 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — Наслаждайся, — хмыкнул он, краем глаза «приглядывая» за уже покрытой следами ржавчины двухдверной «Каплей», чьи потускневшие от времени и грязи фары молодые люди наблюдали в зеркала заднего вида в течение последнего часа.
- current normalized: — Наслаждайся, — хмыкнул он, краем глаза «приглядывая» за уже покрытой следами ржавчины двухдверной «Каплей», чьи потускневшие от времени и грязи фары молодые люди наблюдали в зеркала заднего вида в течение последнего часа.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0020 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все же…
- current normalized: Но всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0020 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Вот еще потом чего-нибудь «лишнего» на десяток грамм и лет десять в придачу найти не хотелось бы.
- current normalized: Вот еще потом чего-нибудь «лишнего» на десяток грамм и лет десять в придачу найти не хотелось бы.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0021 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все также дружелюбно и без какого-либо давления произнес инспектор.
- current normalized: — все также дружелюбно и без какого-либо давления произнес инспектор.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0022 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: С одной стороны, оба могли прекратить все это очень быстро, но с другой…
- current normalized: С одной стороны, оба могли прекратить всё это очень быстро, но с другой…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0025 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Только пусть уж все будет по закону, — добавил клановец.
- current normalized: — Только пусть уж все будет по закону, — добавил клановец.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0027 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все процедуры заняли примерно полчаса.
- current normalized: Все процедуры заняли примерно полчаса.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0039 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: — хмыкнул Павел, глаз на затылке не имевший, а оборачиваться не рискнувший ради конспирации.
- current normalized: — хмыкнул Павел, глаз на затылке не имевший, а оборачиваться не рискнувший ради конспирации.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0050 / `стрелка`
- class: стрелку; verdict: **OK**
- FB2 sentence: Павел же вновь оказался в положении «за стрелка».
- current normalized: Павел же вновь оказался в положении «за стрелка».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0053 / `во-о-о-о-он`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Нам во-о-о-о-он в ту арку, — указал пальцем Волконский.
- current normalized: — Нам вооон в ту арку, — указал пальцем Волконский.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0064 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Преследователь понял все спустя сорок секунд после того, как за его спиной вспыхнули дальним светом фары «Империала».
- current normalized: Преследователь понял все спустя сорок секунд после того, как за его спиной вспыхнули дальним светом фары «Империала».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0068 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Ну вот и все, — выдохнул Павел, наблюдая за тем, как внедорожник его гвардии чуть «приплюснул» двухдверных хэтчбек о стену дома.
- current normalized: — Ну вот и все, — выдохнул Павел, наблюдая за тем, как внедорожник его гвардии чуть «приплюснул» двухдверных хэтчбек о стену дома.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0068 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: — Ну вот и все, — выдохнул Павел, наблюдая за тем, как внедорожник его гвардии чуть «приплюснул» двухдверных хэтчбек о стену дома.
- current normalized: — Ну вот и все, — выдохнул Павел, наблюдая за тем, как внедорожник его гвардии чуть «приплюснул» двухдверных хэтчбек о стену дома.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0008-p-0083 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Клановец еще раз окинул взором «жертву кланового произвола», отдельно «врезая в память» черты лица, и лишь затем со вздохом спросил:
- current normalized: Клановец еще раз окинул взором «жертву кланового произвола», отдельно «врезая в память» черты лица, и лишь затем со вздохом спросил:
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0011 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Девчушка сверкнула глазами.
- current normalized: Девчушка сверкнула глазами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0017 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: «Жертва» с силой зажмурила глаза и тут же распахнула их.
- current normalized: «Жертва» с силой зажмурила глаза и тут же распахнула их.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0034 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: Во всяком случае, глазками она зыркала дюже возмущенно.
- current normalized: Во всяком случае, глазками она зыркала дюже возмущенно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0042 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Александра все поняла правильно.
- current normalized: Александра все поняла правильно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0045 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Лично для меня результат будет един — все равно получу ответы на свои вопросы.
- current normalized: Лично для меня результат будет един — всё равно получу ответы на свои вопросы.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0061 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза Мышкиной тут же распахнулись.
- current normalized: Глаза Мышкиной тут же распахнулись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0077 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все равно достанут.
- current normalized: Всё равно достанут.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0080 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все взгляды сошлись на нем.
- current normalized: Все взгляды сошлись на нем.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0096 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: Не самая, знаете ли, шокирующая новость, произнесенная в этих стенах.
- current normalized: Не самая, знаете ли, шокирующая новость, произнесенная в этих стенах.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0098 / `стенкой`
- class: стены; verdict: **OK**
- FB2 sentence: Просто некоторых людей заложник за стенкой…
- current normalized: Просто некоторых людей заложник за стенкой…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0105 / `стенограмму`
- class: стены; verdict: **OK**
- FB2 sentence: — Сейчас изучу стенограмму допроса, а после, возможно, задам свои, — пообещал молодой человек, куда больше заинтересовавшийся контейнерами с завтраком.
- current normalized: — Сейчас изучу стенограмму допроса, а после, возможно, задам свои, — пообещал молодой человек, куда больше заинтересовавшийся контейнерами с завтраком.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0108 / `Во-о-от`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Во-о-от!
- current normalized: — Вооот!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0111 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И далеко не все представители оных похожи в «демократичности» своей на Павла или Светлану.
- current normalized: И далеко не вс+е представители оных похожи в «демократичности» своей на Павла или Светлану.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0117 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Ей бы демонстративно полюбоваться кадрами, и лишь потом с видом гордым и пафосным заявить о своем несогласии.
- current normalized: Ей бы демонстративно полюбоваться кадрами, и лишь потом с видом гордым и пафосным заявить о своем несогласии.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0124 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: Александра глазками сверкнула, но оспаривать утверждение не спешила.
- current normalized: Александра глазками сверкнула, но оспаривать утверждение не спешила.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0128 / `Потом`
- class: потом; verdict: **OK**
- FB2 sentence: Потом где-то нарыла историю про твои объятия с Ольгой на балу Горюновых.
- current normalized: Потом где-то нарыла историю про твои объятия с Ольгой на балу Горюновых.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0138 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Для чего это все?
- current normalized: — Для чего это все?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0144 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Вот это все еще надо заслужить!
- current normalized: — Вот это всё еще надо заслужить!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0009-p-0147 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: чтобы так оно все и осталось?..
- current normalized: чтобы так оно все и осталось?..
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0011 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Павел, все хорошо?
- current normalized: — Павел, все хорошо?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0021 / `глазастый`
- class: глаза; verdict: **OK**
- FB2 sentence: Конечно, о местных «безах» Волконский был не самого высокого мнения, но вдруг кто глазастый попадется.
- current normalized: Конечно, о местных «безах» Волконский был не самого высокого мнения, но вдруг кто глазастый попадется.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0029 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки, его семья столь высокий статус получила совсем недавно.
- current normalized: Всё-таки, его семья столь высокий статус получила совсем недавно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0052 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ведь никаких доказательств своей личности он не предъявлял, а пропустить в салон авто пусть и младшего наследника «нового» клана, но все-таки охраняемого лица, незнакомца — большая глупость.
- current normalized: Ведь никаких доказательств своей личности он не предъявлял, а пропустить в салон авто пусть и младшего наследника «нового» клана, но всё-таки охраняемого лица, незнакомца — большая глупость.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0052 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Ведь никаких доказательств своей личности он не предъявлял, а пропустить в салон авто пусть и младшего наследника «нового» клана, но все-таки охраняемого лица, незнакомца — большая глупость.
- current normalized: Ведь никаких доказательств своей личности он не предъявлял, а пропустить в салон авто пусть и младшего наследника «нового» клана, но всё-таки охраняемого лица, незнакомца — большая глупость.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Тот нахохлился и все больше закрывался в «броню» отрицания, резко снижая все попытки разумно договориться.
- current normalized: Тот нахохлился и всё больше закрывался в «броню» отрицания, резко снижая все попытки разумно договориться.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Тот нахохлился и все больше закрывался в «броню» отрицания, резко снижая все попытки разумно договориться.
- current normalized: Тот нахохлился и всё больше закрывался в «броню» отрицания, резко снижая все попытки разумно договориться.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0070 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Впрочем, через секунду глаза Дмитрия распахнулись в понимании.
- current normalized: Впрочем, через секунду глаза Дмитрия распахнулись в понимании.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0080 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Родился с серебряной ложкой в заднице и считаешь, что все можно, да⁈
- current normalized: — Родился с серебряной ложкой в заднице и считаешь, что все можно, да?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0084 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Забрали себе все, а нам бросили объедки!
- current normalized: — Забрали себе все, а нам бросили объедки!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0111 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: — Присаживайся, сын, — предложил отец, рассматривая городские пейзажи с высоты птичьего полета.
- current normalized: — Присаживайся, сын, — предложил отец, рассматривая городские пейзажи с высоты птичьего полета.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0120 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки ее репутация на кону.
- current normalized: Всё-таки ее репутация на кону.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0010-p-0125 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Вот только все это дела далеких дней.
- current normalized: Вот только всё это дела далеких дней.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Немолодая, но все еще статная женщина смерила равнодушным взглядом типичного обитателя местных бараков.
- current normalized: Немолодая, но всё еще статная женщина смерила равнодушным взглядом типичного обитателя местных бараков.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0005 / `глазницу`
- class: глаза; verdict: **OK**
- FB2 sentence: Ее легко можно было представить с указкой у школьной доски, но куда сложнее было вообразить ее человеком, без особых колебаний готовым засунуть указательный палец на всю возможную глубину в глазницу врага.
- current normalized: Ее легко можно было представить с указкой у школьной доски, но куда сложнее было вообразить ее человеком, без особых колебаний готовым засунуть указательный палец на всю возможную глубину в глазницу врага.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0011 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: В глазах довольно скромно, но опрятно одетой «старухи»…
- current normalized: В глазах довольно скромно, но опрятно одетой «старухи»…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0022 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: — фыркнул облокотившийся на стену огромный и бородатый, но отчего-то с первого взгляда незамеченный, Магомед.
- current normalized: — фыркнул облокотившийся на стену огромный и бородатый, но отчего-то с первого взгляда незамеченный, Магомед.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0026 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Почти все на месте!
- current normalized: «Почти все на месте!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0028 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Однако спокойный взгляд умных глаз и четкая моторика ясно давали понять, что списывать со счетов его пока рано.
- current normalized: Однако спокойный взгляд умных глаз и четкая моторика ясно давали понять, что списывать со счетов его пока рано.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0040 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако одно дело работать с мыслью о том, что за твоими плечами все же стоит государство, и совершенно иной коленкор «химичить» в…
- current normalized: Однако одно дело работать с мыслью о том, что за твоими плечами всё же стоит государство, и совершенно иной коленкор «химичить» в…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0041 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Он уже все долги империи отдал.
- current normalized: Он уже все долги империи отдал.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0050 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Но правила все те же, — уставился на него бывший командир.
- current normalized: — Но правила все те же, — уставился на него бывший командир.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0052 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Алексея все трое заметили сразу.
- current normalized: Алексея все трое заметили сразу.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0059 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все также синхронно и столь же скупо.
- current normalized: Все также синхронно и столь же скупо.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0059 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Оба были профессионалами, и прекрасно понимали, что стоит им сейчас лишь дать повод заподозрить себя в «нелояльности» и все закончится плохо.
- current normalized: Оба были профессионалами, и прекрасно понимали, что стоит им сейчас лишь дать повод заподозрить себя в «нелояльности» и все закончится плохо.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0060 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В них все необходимое: деньги, средства связи, инструменты.
- current normalized: В них всё необходимое: деньги, средства связи, инструменты.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0081 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — со всей возможной искренностью постарался сделать невинный вид Волконский, уже прекрасно понимая, к чему именно все идет.
- current normalized: — со всей возможной искренностью постарался сделать невинный вид Волконский, уже прекрасно понимая, к чему именно все идет.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0085 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все компоненты можно найти в ближайшем хозяйственном магазине.
- current normalized: Все компоненты можно найти в ближайшем хозяйственном магазине.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0087 / `СВУ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Так что собрать СВУ из подручных средств парень смог бы на раз.
- current normalized: Так что собрать СВУ из подручных средств парень смог бы на раз.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0090 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Это все прекрасно, милая моя, — вновь обернулся к Тишь Волконский, вызвав одобрительный смешок у сапера, явно наслаждавшегося пикировкой.
- current normalized: — Это все прекрасно, милая моя, — вновь обернулся к Тишь Волконский, вызвав одобрительный смешок у сапера, явно наслаждавшегося пикировкой.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0091 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки подобное происшествие скорее по ведомству городской полиции проходит.
- current normalized: Всё-таки подобное происшествие скорее по ведомству городской полиции проходит.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0091 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Но никак не СИБ.
- current normalized: Но никак не СИБ.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0102 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки не зря же они здесь собрались.
- current normalized: Всё-таки не зря же они здесь собрались.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0106 / `СВУ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — Личность, класс сборки СВУ, и сам факт, — коротко перечислила девушка, сложив руки на груди.
- current normalized: — Личность, класс сборки СВУ, и сам факт, — коротко перечислила девушка, сложив руки на груди.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0122 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но, как правило, все же достигает логического завершения.
- current normalized: Но, как правило, всё же достигает логического завершения.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0123 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Мы же через несколько секунд не только получили все данные об убитом, но и имеем достаточно уцелевшего материала для экспертизы.
- current normalized: — Мы же через несколько секунд не только получили все данные об убитом, но и имеем достаточно уцелевшего материала для экспертизы.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0126 / `ма-а-аленький`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Вот и думай, Шут, вот и думай, — откинулась на спинку пассажирского сидения культуристка, вполне явно намекая на тот ма-а-аленький факт, что очень уж удачно на месте происшествия оказался сотрудник, который хоть что-то да знал о группе Фролова.
- current normalized: — Вот и думай, Шут, вот и думай, — откинулась на спинку пассажирского сидения культуристка, вполне явно намекая на тот маааленький факт, что очень уж удачно на месте происшествия оказался сотрудник, который хоть что-то да знал о группе Фролова.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0132 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все в порядке, Рома, — чуть удивленно подняла голову Волконская, отрывая взгляд от очередного отчета.
- current normalized: — Все в порядке, Рома, — чуть удивленно подняла голову Волконская, отрывая взгляд от очередного отчета.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0134 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Когда «все в порядке», — глухо произнес он.
- current normalized: — Когда «все в порядке», — глухо произнес он.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0135 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Цвета ночи микроавтобус с эмблемой СИБ был не у «ворот», а прямо перед заводоуправлением.
- current normalized: Цвета ночи микроавтобус с эмблемой СИБ был не у «ворот», а прямо перед заводоуправлением.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0137 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако молодой мужчина все-таки взял себя в руки и с расспросами не полез.
- current normalized: Однако молодой мужчина всё-таки взял себя в руки и с расспросами не полез.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0152 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Пока же просто можно радоваться возможности встретиться с родичами без предварительной подготовки с участием СИБ.
- current normalized: Пока же просто можно радоваться возможности встретиться с родичами без предварительной подготовки с участием СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0166 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Если мне все мозги «сотрясут», то я тебе помочь не смогу!
- current normalized: — Если мне все мозги «сотрясут», то я тебе помочь не смогу!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0174 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ты же сказал, все будет тихо и спокойно!
- current normalized: Ты же сказал, все будет тихо и спокойно!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0174 / `Та-а-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-а-ак, братец!
- current normalized: — Тааак, братец!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0176 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мол, все-все знаю, но ничего никому не скажу!
- current normalized: Мол, все-все знаю, но ничего никому не скажу!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0011-p-0176 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мол, все-все знаю, но ничего никому не скажу!
- current normalized: Мол, все-все знаю, но ничего никому не скажу!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0008 / `о-о-о-очень`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — о-о-о-очень задумчивого Главу клана, плюхнувшего прямо на лавку уличного столика с какими-то бумагами в руках;
- current normalized: — ооочень задумчивого Главу клана, плюхнувшего прямо на лавку уличного столика с какими-то бумагами в руках;
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0026 / `высотном`
- class: высоты; verdict: **OK**
- FB2 sentence: — Допустим, «налог на проживание и содержание имущества в родовом высотном доме» я еще…
- current normalized: — Допустим, «налог на проживание и содержание имущества в родовом высотном доме» я еще…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0026 / `Та-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-ак, — вздохнул Игорь Георгиевич, поняв, что над ним брат не смеется.
- current normalized: — Тааак, — вздохнул Игорь Георгиевич, поняв, что над ним брат не смеется.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0029 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Налог платили все.
- current normalized: Налог платили все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0032 / `Та-а-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-а-ак, — продолжил тот.
- current normalized: — Тааак, — продолжил тот.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0035 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Мужчина быстренько пробежал глазами первую страницу и…
- current normalized: Мужчина быстренько пробежал глазами первую страницу и…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0044 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — А ты точно все прочитал?
- current normalized: — А ты точно все прочитал?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0047 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: По мере чтения брови его ползли к волосам все отчетливее.
- current normalized: По мере чтения брови его ползли к волосам все отчетливее.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0050 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Нет, я все понимаю…
- current normalized: — Нет, я все понимаю…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0054 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Собственно, с него все и началось…
- current normalized: Собственно, с него все и началось…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0055 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Наверное, все-таки начало безобразию положил все же Глава, решивший, вопреки всяческим правилам и регламентам, проявить демократичность и встретить «детишек» у машины.
- current normalized: Наверное, всё-таки начало безобразию положил всё же Глава, решивший, вопреки всяческим правилам и регламентам, проявить демократичность и встретить «детишек» у машины.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0055 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Наверное, все-таки начало безобразию положил все же Глава, решивший, вопреки всяческим правилам и регламентам, проявить демократичность и встретить «детишек» у машины.
- current normalized: Наверное, всё-таки начало безобразию положил всё же Глава, решивший, вопреки всяческим правилам и регламентам, проявить демократичность и встретить «детишек» у машины.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0057 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: — Маска для лица, — хмыкнул человек, погружая «комитет по встрече» в некоторую задумчивость.
- current normalized: — Маска для лица, — хмыкнул человек, погружая «комитет по встрече» в некоторую задумчивость.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0059 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — О, все просто, — тут же оживился юноша.
- current normalized: — О, все просто, — тут же оживился юноша.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0059 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: и лицо тут же начинает улыбаться и свежеть прямо на глазах!
- current normalized: и лицо тут же начинает улыбаться и свежеть прямо на глазах!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все же уточнил настырный дядька.
- current normalized: — всё же уточнил настырный дядька.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0071 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Правда, знали об этом далеко не все.
- current normalized: Правда, знали об этом далеко не все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0075 / `О-О-О-ОЧЕНЬ`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Девушка О-О-О-ОЧЕНЬ рекомендовала обойтись без экспериментов.
- current normalized: Девушка ОООЧЕНЬ рекомендовала обойтись без экспериментов.
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0012-p-0078 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Его все сразу поняли правильно.
- current normalized: Его все сразу поняли правильно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0009 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В курсе предстоящей свадьбы были все.
- current normalized: В курсе предстоящей свадьбы были все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0013 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все присутствующие понимали разницу в положении Кошкиной и Юсуповой.
- current normalized: Все присутствующие понимали разницу в положении Кошкиной и Юсуповой.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0013 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все это считывалось окружающими.
- current normalized: И всё это считывалось окружающими.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0015 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: Уралочка же просто распахнула глазки и застыла.
- current normalized: Уралочка же просто распахнула глазки и застыла.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0017 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Павел вздохнул и прикрыл глаза.
- current normalized: Павел вздохнул и прикрыл глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0018 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ведь нормально же все было!
- current normalized: Ведь нормально же все было!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0018 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И даже не огрызалась в сторону Лены, а Катерине хоть и обещала избавиться от нее при первой возможности, но все же не упускала шанса прикоснуться к ее кулинарному искусству…
- current normalized: И даже не огрызалась в сторону Лены, а Катерине хоть и обещала избавиться от нее при первой возможности, но всё же не упускала шанса прикоснуться к ее кулинарному искусству…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0018 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: в общем, все было довольно мирно.
- current normalized: в общем, все было довольно мирно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0023 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза Светланы блеснули сталью ничуть не хуже, чем у брата.
- current normalized: Глаза Светланы блеснули сталью ничуть не хуже, чем у брата.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0044 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Уже все СМИ объявили, что мы с тобой…
- current normalized: — Уже все СМИ объявили, что мы с тобой…
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0063 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: Однако глазки у Юсуповой в миг, когда она деревянной походкой покидала Главный зал, были широко распахнуты.
- current normalized: Однако глазки у Юсуповой в миг, когда она деревянной походкой покидала Главный зал, были широко распахнуты.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0064 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Будем надеяться, проняло, — все же дежурно обозначил улыбку Павел.
- current normalized: — Будем надеяться, проняло, — всё же дежурно обозначил улыбку Павел.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0066 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Посидев без движения пару секунд, молодой человек приоткрыл глаза и уверенно кивнул.
- current normalized: Посидев без движения пару секунд, молодой человек приоткрыл глаза и уверенно кивнул.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0097 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Будущий Глава клана на миг развеселился, в красках представив скандал, который устроит Юсупова отцу, когда все всплывет наружу.
- current normalized: Будущий Глава клана на миг развеселился, в красках представив скандал, который устроит Юсупова отцу, когда все всплывет наружу.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0013-p-0101 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Игнат все и так прекрасно понял.
- current normalized: Игнат все и так прекрасно понял.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0003 / `Ка-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ка-а-а-ак…
- current normalized: — Кааак…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: С каждым годом география и характер задач становились все более разнообразными, пока однажды Тарга не получила сигнал «Воздух».
- current normalized: С каждым годом география и характер задач становились все более разнообразными, пока однажды Тарга не получила сигнал «Воздух».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0023 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако все-таки поддался на «уговоры» и провернулся.
- current normalized: Однако всё-таки поддался на «уговоры» и провернулся.
- current rule: `phrase.lock_context, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0023 / `замок`
- class: замок; verdict: **OK**
- FB2 sentence: За много лет простоя замок явно не желал открываться.
- current normalized: За много лет простоя зам+ок явно не желал открываться.
- current rule: `phrase.lock_context, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0052 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: разве что Лом все равно сыграл бы свою роль.
- current normalized: разве что Лом всё равно сыграл бы свою роль.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0055 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Это еще не все новости, — обрадовал Ольгу Барон.
- current normalized: — Это еще не все новости, — обрадовал Ольгу Барон.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0057 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: все сложнее.
- current normalized: все сложнее.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0061 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Этот странный ритм вызвал куда больше интереса, чем все предыдущие слова.
- current normalized: Этот странный ритм вызвал куда больше интереса, чем все предыдущие слова.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — И, буду с вами честен, не могу обещать, что все получится.
- current normalized: — И, буду с вами честен, не могу обещать, что все получится.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0071 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В этот раз (и все это прекрасно понимали!
- current normalized: В этот раз (и всё это прекрасно понимали!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0073 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Зато все теперь знали, что командир под «поводком» столь плотным, что и в носу не может поковыряться без того, чтобы неизвестный «контролер» не узнал, насколько глубоко был засунут палец и с какой интенсивностью проворачивается.
- current normalized: Зато все теперь знали, что командир под «поводком» столь плотным, что и в носу не может поковыряться без того, чтобы неизвестный «контролер» не узнал, насколько глубоко был засунут палец и с какой интенсивностью проворачивается.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0076 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Приятно знать, что соратники все так же остаются на твоей стороне.
- current normalized: Приятно знать, что соратники всё так же остаются на твоей стороне.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0078 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: По мере того как до них доходила простая, в общем-то, мысль, лица их демонстрировали некую степень удивления.
- current normalized: По мере того как до них доходила простая, в общем-то, мысль, лица их демонстрировали некую степень удивления.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0084 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Я все слышу, — спокойно объявила Виктория и…
- current normalized: — Я все слышу, — спокойно объявила Виктория и…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0084 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: все.
- current normalized: все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0087 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но тут же отбросил все сомнения.
- current normalized: Но тут же отбросил все сомнения.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0087 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки за процессом зорко наблюдал его личный светловолосый ангел-хранитель.
- current normalized: Всё-таки за процессом зорко наблюдал его личный светловолосый ангел-хранитель.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0094 / `Кха-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Кха-а-а-а…
- current normalized: — Кхааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0014-p-0098 / `Кха-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Кха-а-а-а!..
- current normalized: — Кхааа!..
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0010 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Не все так плохо, — произнесла Мышкина негромко.
- current normalized: — Не все так плохо, — произнесла Мышкина негромко.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0012 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все хорошо, — не так чтобы очень уверенно попробовала она еще раз.
- current normalized: — Все хорошо, — не так чтобы очень уверенно попробовала она еще раз.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0013 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Поймал ее все-таки Волконский.
- current normalized: Поймал ее всё-таки Волконский.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ведь все это появилось относительно недавно.
- current normalized: Ведь всё это появилось относительно недавно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако почти все доходы тут же реинвестировал в еще только набирающую вес медиаимперию.
- current normalized: Однако почти все доходы тут же реинвестировал в еще только набирающую вес медиаимперию.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0015 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все эти дорогие машины, личный спортивный глайдер, шмотки от лучших дизайнеров мира и безлимитная карточка появились в жизни Мышкиной совсем недавно.
- current normalized: Все эти дорогие машины, личный спортивный глайдер, шмотки от лучших дизайнеров мира и безлимитная карточка появились в жизни Мышкиной совсем недавно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И впервые она столкнулась с ситуацией, когда все это могло буквально раствориться по одному щелчку пальцев родовитого засранца.
- current normalized: И впервые она столкнулась с ситуацией, когда всё это могло буквально раствориться по одному щелчку пальцев родовитого засранца.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0033 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: — А потом?
- current normalized: — А пот+ом?
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0035 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: — А потом я сделаю Светлане Анатольевне Волконской небольшой подарок, — предвкушающе улыбнулся молодой человек.
- current normalized: — А пот+ом я сделаю Светлане Анатольевне Волконской небольшой подарок, — предвкушающе улыбнулся молодой человек.
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0036 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Просто отчего-то все были уверены, что стоит перейти дорогу Волконской, и она сломает жизнь обидчика.
- current normalized: Просто отчего-то вс+е были уверены, что стоит перейти дорогу Волконской, и она сломает жизнь обидчика.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0038 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: — А потом?
- current normalized: — А пот+ом?
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0045 / `Потом`
- class: потом; verdict: **OK**
- FB2 sentence: Потом я позвоню любимой сестренке!
- current normalized: Потом я позвоню любимой сестренке!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0047 / `Э-э-эй`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Э-э-эй!
- current normalized: — ЭЭЭй!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0052 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все, — коротко ответила Александра, вдруг прекрасно осознав, что именно так дело и обстоит.
- current normalized: — Все, — коротко ответила Александра, вдруг прекрасно осознав, что именно так дело и обстоит.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0060 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Впрочем, еще через секунду она решила, что никогда и никому об этом рассказывать все же не будет.
- current normalized: Впрочем, еще через секунду она решила, что никогда и никому об этом рассказывать всё же не будет.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0060 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Скажи кому, что она своими глазами видела «фейспалм» в исполнении наследника Волконских — не поверят.
- current normalized: Скажи кому, что она своими глазами видела «фейспалм» в исполнении наследника Волконских — не поверят.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0064 / `Да-а-а-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Да-а-а-а-а-а…
- current normalized: — Дааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0093 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: Аж глазки зажмурила и…
- current normalized: Аж глазки зажмурила и…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0100 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: да вообще на все!
- current normalized: да вообще на все!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0101 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: — Они же меня запытают потом!
- current normalized: — Они же меня запытают потом!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0103 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза девушки удивленно распахнулись.
- current normalized: Глаза девушки удивленно распахнулись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0118 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: » — решила мысленно милая воспитанная девушка, вновь закрывая глаза.
- current normalized: » — решила мысленно милая воспитанная девушка, вновь закрывая глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0119 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Кое-кто совсем недавно заявил, что готов на все.
- current normalized: — Кое-кто совсем недавно заявил, что готов на все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0120 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Может, все-таки оргия?
- current normalized: — Может, всё-таки оргия?
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0124 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Можешь успокоиться, выбора у тебя все равно нет, — как само собой разумеющееся констатировал клановец.
- current normalized: — Можешь успокоиться, выбора у тебя всё равно нет, — как само собой разумеющееся констатировал клановец.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0015-p-0128 / `статью`
- class: статью; verdict: **OK**
- FB2 sentence: — Ты эту статью переживешь.
- current normalized: — Ты эту статью переживешь.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0006 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Не обращай внимания, да и все.
- current normalized: — Не обращай внимания, да и все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0007 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А уж в обеденном зале так и вовсе можно было пялиться лишь на «принцессу» и все равно держать в поле зрения еще и брата с сестрой.
- current normalized: А уж в обеденном зале так и вовсе можно было пялиться лишь на «принцессу» и всё равно держать в поле зрения еще и брата с сестрой.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0009 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но она уже успела оценить все прелести «непротокольного» общения, и с удовольствием пользовалась расширившимися возможностями.
- current normalized: Но она уже успела оценить все прелести «непротокольного» общения, и с удовольствием пользовалась расширившимися возможностями.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0016 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако «шило», как ему и полагается в «мешке» довольно замкнутого коллектива, все равно вылезло наружу.
- current normalized: Однако «шило», как ему и полагается в «мешке» довольно замкнутого коллектива, всё равно вылезло наружу.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0025 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мы все умрем!
- current normalized: Мы все умрем!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0025 / `статью`
- class: статью; verdict: **OK**
- FB2 sentence: Клановец даже не стал открывать статью.
- current normalized: Клановец даже не стал открывать статью.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0025 / `А-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Сразу после выступления из серии «А-а-а-а!..
- current normalized: Сразу после выступления из серии «ААА!..
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0032 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Неужели восприняла все столь близко к сердцу?
- current normalized: — Неужели восприняла все столь близко к сердцу?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0034 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Так понимаю, ты все еще рассчитываешь пока остаться холостым?
- current normalized: — Так понимаю, ты всё еще рассчитываешь пока остаться холостым?
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0062 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки будущую элиту империи хранили как зеницу ока.
- current normalized: Всё-таки будущую элиту империи хранили как зеницу ока.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0063 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все не пьянства ради, а исключительно с целью подлечить чуть пошатнувшиеся нервы.
- current normalized: Все не пьянства ради, а исключительно с целью подлечить чуть пошатнувшиеся нервы.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: сам все понимаешь.
- current normalized: сам все понимаешь.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0088 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Думаю, там найдется все, что нужно.
- current normalized: Думаю, там найдется все, что нужно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0091 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Тарга сосредоточенно глянула в глаза командира.
- current normalized: Тарга сосредоточенно глянула в глаза командира.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0016-p-0096 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: В глазах его на миг блеснуло удовлетворение из серии «я понял, что ты поняла, а ты поняла…
- current normalized: В глазах его на миг блеснуло удовлетворение из серии «я понял, что ты поняла, а ты поняла…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0003 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — То не досочки, то косточки трещат, — хмыкнул Павел, ни в какую не желая открывать глаза.
- current normalized: — То не досочки, то косточки трещат, — хмыкнул Павел, ни в какую не желая открывать глаз+а.
- current rule: `phrase.eyes`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0007 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Для следующей операции ему глаз открыть пришлось.
- current normalized: Для следующей операции ему глаз открыть пришлось.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0008 / `Та-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-ак…
- current normalized: — Тааак…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0009 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Пару раз он таки промахнулся мимо иконки, но все же справился с непростой удумкою военных инженеров клана.
- current normalized: Пару раз он таки промахнулся мимо иконки, но всё же справился с непростой удумкою военных инженеров клана.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0010 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: норм, — решил Павел, все также одним глазом оценив результат.
- current normalized: норм, — решил Павел, все также одним глазом оценив результат.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0010 / `глазом`
- class: глаза; verdict: **OK**
- FB2 sentence: норм, — решил Павел, все также одним глазом оценив результат.
- current normalized: норм, — решил Павел, все также одним глазом оценив результат.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0010 / `Ну-у-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну-у-у-у-у…
- current normalized: — Нууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0011 / `среду`
- class: среду; verdict: **OK**
- FB2 sentence: Пальцы практически без участия мозга набрали короткое сообщение: «А как ты проводишь свою среду⁈
- current normalized: Пальцы практически без участия мозга набрали короткое сообщение: «А как ты проводишь свою ср+еду?!
- current rule: `phrase.medium_day_context, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0016 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все еще спишь, что ли⁈
- current normalized: — Всё еще спишь, что ли?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0029 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Не все тогда сумели своевременно понять, что «инструменты» существуют ради убийства «дракона», а вовсе не для того, чтобы занять его место.
- current normalized: Не все тогда сумели своевременно понять, что «инструменты» существуют ради убийства «дракона», а вовсе не для того, чтобы занять его место.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0030 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Судя по всему, все виновные были «наказаны».
- current normalized: Судя по всему, все виновные были «наказаны».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0036 / `Пу-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Пу-у-у-у-пу-пу-пу-пу-у-у-у…
- current normalized: — Пууу-пу-пу-пу-пууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0036 / `пу-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Пу-у-у-у-пу-пу-пу-пу-у-у-у…
- current normalized: — Пууу-пу-пу-пу-пууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0036 / `Та-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Та-а-а-ак…
- current normalized: что я упустил?
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0042 / `стрелковой`
- class: стрелку; verdict: **OK**
- FB2 sentence: Культуристка прекрасно помнила слова одного из собственных инструкторов по стрелковой подготовке: «Таких уже не делают!
- current normalized: Культуристка прекрасно помнила слова одного из собственных инструкторов по стрелковой подготовке: «Таких уже не делают!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0048 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — тут же защебетала девушка, едва не размазавшая мужчину между капотом своей «крошки» и бортом транспорта СИБ.
- current normalized: — тут же защебетала девушка, едва не размазавшая мужчину между капотом своей «крошки» и бортом транспорта СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0053 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Ну, есть такое, — кивнул Павел, все еще не сообразивший, какое вообще отношение имеет его сон к делу.
- current normalized: — Ну, есть такое, — кивнул Павел, всё еще не сообразивший, какое вообще отношение имеет его сон к делу.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0059 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Можно будет потом шепнуть на ушко Константину Дмитриевичу, что именно он думает о подобных приказах.
- current normalized: Можно будет потом шепнуть на ушко Константину Дмитриевичу, что именно он думает о подобных приказах.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0067 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В случае неудачи же мне куда больше поможет искусство грамотного с***а, а не вот это вот все.
- current normalized: а, а не вот это вот все.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Ну все, не спи!
- current normalized: — Ну все, не спи!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0082 / `никого не было`
- class: не было; verdict: **OK**
- FB2 sentence: рядом никого не было.
- current normalized: рядом никого н+е было.
- current rule: `phrase.ne_bylo`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0085 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: На миг все мышцы Тарги напряглись тугими канатами и…
- current normalized: На миг все мышцы Тарги напряглись тугими канатами и…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0089 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако сколько не натягивай на гражданского «сбрую», все равно будет видно, что он в ней чувствует себя неуютно.
- current normalized: Однако сколько не натягивай на гражданского «сбрую», всё равно будет видно, что он в ней чувствует себя неуютно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0104 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Спецы, уже прекрасно осознавшие, что все «фигуры» на игровой доске, спокойно разорвали дистанцию, буквально через несколько секунд скрывшись из виду.
- current normalized: Спецы, уже прекрасно осознавшие, что все «фигуры» на игровой доске, спокойно разорвали дистанцию, буквально через несколько секунд скрывшись из виду.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0105 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — поинтересовалась Ольга, все не терявшая надежды «качнуть» собеседника.
- current normalized: — поинтересовалась Ольга, все не терявшая надежды «качнуть» собеседника.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0110 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: раз уж вы здесь, то предлагаю решить, как именно мы с вами все это провернем.
- current normalized: раз уж вы здесь, то предлагаю решить, как именно мы с вами всё это провернем.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0017-p-0113 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: И еще совсем недавно Хранитель ключей мог бы с уверенностью сказать, что за всю свою длинную и насыщенную жизнь он еще ни разу не слышал в этих стенах…
- current normalized: И еще совсем недавно Хранитель ключей мог бы с уверенностью сказать, что за всю свою длинную и насыщенную жизнь он еще ни разу не слышал в этих стенах…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0003 / `стен`
- class: стены; verdict: **OK**
- FB2 sentence: Просто потому, что ЭТО учебное заведение не выдаст никакой информации о произошедшем внутри его стен даже Волконским.
- current normalized: Просто потому, что ЭТО учебное заведение не выдаст никакой информации о произошедшем внутри его стен даже Волконским.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0009 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: Незавидная участь залетчика в стенах этого заведения.
- current normalized: Незавидная участь залетчика в стенах этого заведения.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0009 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: А уж если на пути за стены сего замечательного «притона» совершить одну из тех милых ошибок, что преподаватели именуют исключительно эпитетом «тупые», то жизнь может осложниться всерьез.
- current normalized: А уж если на пути за стены сего замечательного «притона» совершить одну из тех милых ошибок, что преподаватели именуют исключительно эпитетом «тупые», то жизнь может осложниться всерьез.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0019 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все и так прекрасно знали, чем именно промышляет этот хитрый Лис.
- current normalized: Все и так прекрасно знали, чем именно промышляет этот хитрый Лис.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0022 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И это пусть и компактной, но все же сумкой.
- current normalized: И это пусть и компактной, но всё же сумкой.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0022 / `СВУ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Хотя бы потому что в этой самой сумке могло находиться СВУ с импровизированными поражающими элементами.
- current normalized: Хотя бы потому что в этой самой сумке могло находиться СВУ с импровизированными поражающими элементами.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0024 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Хотя, конечно, какие-то демонстративные взыскания все-таки наложат.
- current normalized: Хотя, конечно, какие-то демонстративные взыскания всё-таки наложат.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0028 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Каждый подобный случай — повод для организации группы разбора, костяк которой обычно состоял из представителей инструкторского штаба, СИБ, Канцелярии и привлеченных "отраслевых специалистов.
- current normalized: Каждый подобный случай — повод для организации группы разбора, костяк которой обычно состоял из представителей инструкторского штаба, СИБ, Канцелярии и привлеченных "отраслевых специалистов.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0028 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: И вся эта свора буквально наизнанку вывернет бегунка, чтобы понять, как именно и что именно ему удалось провернуть, чтобы после выдать рекомендации СБ СИБ, а иногда даже и соответствующим службам страны и армии.
- current normalized: И вся эта свора буквально наизнанку вывернет бегунка, чтобы понять, как именно и что именно ему удалось провернуть, чтобы после выдать рекомендации СБ СИБ, а иногда даже и соответствующим службам страны и армии.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0029 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: Но Сергей был готов заплатить такую цену за возможность доставить редкий в этих стенах груз в учебное заведение.
- current normalized: Но Сергей был готов заплатить такую цену за возможность доставить редкий в этих стенах груз в учебное заведение.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0041 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: К удивлению мученицы науки, клановец даже не отпрянул в сторону, заглянув ей в глаза.
- current normalized: К удивлению мученицы науки, клановец даже не отпрянул в сторону, заглянув ей в глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0043 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В конце концов, давно уже обоим все понятно.
- current normalized: В конце концов, давно уже обоим все понятно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0045 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Заткнуться и плыть по течению — вот единственная правильная линия поведения с уже все для себя решившей девушкой.
- current normalized: Заткнуться и плыть по течению — вот единственная правильная линия поведения с уже все для себя решившей девушкой.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0046 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все это время Марика сосредоточенно сопела, но начинать разговор не желала.
- current normalized: Всё это время Марика сосредоточенно сопела, но начинать разговор не желала.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0048 / `стен`
- class: стены; verdict: **OK**
- FB2 sentence: Так что стол получился пусть и не слишком радующий обилием разносолов, но для этих стен вполне себе приличный!
- current normalized: Так что стол получился пусть и не слишком радующий обилием разносолов, но для этих стен вполне себе приличный!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0060 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Конечно, будь бы у молодого человека возможность, он обязательно бы заперся на все засовы.
- current normalized: Конечно, будь бы у молодого человека возможность, он обязательно бы заперся на все засовы.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0065 / `эээ`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: эээ…
- current normalized: эээ…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0066 / `Эээ`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: «Эээ» несколько секунд не шевелилась.
- current normalized: «Эээ» несколько секунд не шевелилась.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0068 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Просто он, в отличие от любовавшихся попкой Марики, смотрел в настолько безмятежно-спокойные глаза девушки, что ему натурально становилось страшно.
- current normalized: Просто он, в отличие от любовавшихся попкой Марики, смотрел в настолько безмятежно-спокойные глаза девушки, что ему натурально становилось страшно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0073 / `стеной`
- class: стены; verdict: **OK**
- FB2 sentence: Именно в таком положении он и встретился со стеной в коридоре.
- current normalized: Именно в таком положении он и встретился со стеной в коридоре.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0074 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: А еще командир тройки буквально раздирался между желанием хоть краем глаза посмотреть, что именно там происходит и слаженным хором рассудка и инстинкта самосохранения, на пару убеждавшим его, что лучше свалить отсюда подальше.
- current normalized: А еще командир тройки буквально раздирался между желанием хоть краем глаза посмотреть, что именно там происходит и слаженным хором рассудка и инстинкта самосохранения, на пару убеждавшим его, что лучше свалить отсюда подальше.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0076 / `глазом`
- class: глаза; verdict: **OK**
- FB2 sentence: Судя по тому, как он держался за лицо, «подсветил» ему верное решение будущий шикарный бланш под левым глазом.
- current normalized: Судя по тому, как он держался за лицо, «подсветил» ему верное решение будущий шикарный бланш под левым глазом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0081 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глядя прямо в глаза девушке, он демонстративно спрятал за спину журнал.
- current normalized: Глядя прямо в глаза девушке, он демонстративно спрятал за спину журнал.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0092 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глядя в сверкающие глаза Орловой, Сергей решил, что если бы у него и были какие сомнения, то СЕЙЧАС он возражать бы точно не стал!
- current normalized: Глядя в сверкающие глаза Орловой, Сергей решил, что если бы у него и были какие сомнения, то СЕЙЧАС он возражать бы точно не стал!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0104 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки после бессонной ночи кофеин — самое оно.
- current normalized: Всё-таки после бессонной ночи кофеин — самое оно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0108 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В итоге пришлось разбить «мозговитых» на две группы (Света и все остальные), после этого дело пошло…
- current normalized: В итоге пришлось разбить «мозговитых» на две группы (Света и все остальные), после этого дело пошло…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0110 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Лишь липкая горечь на языке оставляла столь острое желание сплюнуть, что глаза поневоле открылись.
- current normalized: Лишь липкая горечь на языке оставляла столь острое желание сплюнуть, что глаза поневоле открылись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0111 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Но окончательное утверждение операции после изучения выкладок группой СИБ.
- current normalized: Но окончательное утверждение операции после изучения выкладок группой СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0120 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Чем СИБ занимается⁈
- current normalized: Чем СИБ занимается?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0123 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Можно кичиться вековыми традициями сколько угодно пока все хорошо.
- current normalized: — Можно кичиться вековыми традициями сколько угодно пока все хорошо.
- current rule: `phrase.potom, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0123 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Сами работать мешают, а потом…
- current normalized: Сами работать мешают, а пот+ом…
- current rule: `phrase.potom, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0128 / `во-о-от`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну во-о-от, — с укоризной протянула клановец.
- current normalized: — Ну вооот, — с укоризной протянула клановец.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0130 / `нападавших`
- class: нападавших; verdict: **OK**
- FB2 sentence: — Кто-то же должен прийти и убить всех нападавших?
- current normalized: — Кто-то же должен прийти и убить всех нападавших?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0018-p-0135 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Смысл спорить, если руководство все решило.
- current normalized: Смысл спорить, если руководство все решило.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0002 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все купила?
- current normalized: — Все купила?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0013 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В комнате, «назначенной» кают-компанией собрались все через полминуты.
- current normalized: В комнате, «назначенной» кают-компанией собрались все через полминуты.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0014 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Бойцы группы собрались возле все того же журнального столика и внимательно уставились на героиню дня.
- current normalized: Бойцы группы собрались возле всё того же журнального столика и внимательно уставились на героиню дня.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0019 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — СИБ.
- current normalized: — СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0024 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все же…
- current normalized: Но всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0028 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Я передала ему все что нужно.
- current normalized: Я передала ему все что нужно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0030 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Чего случится с таким «золотым мальчиком» — потом не отмоешься.
- current normalized: Чего случится с таким «золотым мальчиком» — потом не отмоешься.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0031 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Хотя он и предупредил, что ведет запись для СИБ.
- current normalized: Хотя он и предупредил, что ведет запись для СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0032 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Не отводя взгляда от задумчивых глаз командира, Тарга избавила часть шоколадной плитки от фольги.
- current normalized: Не отводя взгляда от задумчивых глаз командира, Тарга избавила часть шоколадной плитки от фольги.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0047 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Он не страдал нарушениями слуха, а потому прекрасно все понял.
- current normalized: Он не страдал нарушениями слуха, а потому прекрасно все понял.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0061 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: В СИБ формируют следственную группу.
- current normalized: В СИБ формируют следственную группу.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0062 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Хотя все понимали, что разговор еще не закончен.
- current normalized: Хотя вс+е понимали, что разговор еще не закончен.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0065 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: — Ха, — едва слышно выдохнул он, швырнув огрызок яблока в стену.
- current normalized: — Ха, — едва слышно выдохнул он, швырнув огрызок яблока в стену.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0066 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но хоть все же…
- current normalized: Но хоть всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0068 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А потому, едва пришел сигнал на расформирование группы, Барон отдал последний приказ, прежде чем обрубить все ведущие к нему ниточки: залечь на дно.
- current normalized: А потому, едва пришел сигнал на расформирование группы, Барон отдал последний приказ, прежде чем обрубить все ведущие к нему ниточки: залечь на дно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0077 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все это уже не говоря о такой мелочи, что, на секундочку, никто столь дедовским способом пол давно не моет.
- current normalized: И всё это уже не говоря о такой мелочи, что, на секундочку, никто столь дедовским способом пол давно не моет.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0079 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: С этими словами молодой человек протянул привратнице официальный бланк, подписанный представителем СИБ при Классах.
- current normalized: С этими словами молодой человек протянул привратнице официальный бланк, подписанный представителем СИБ при Классах.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0083 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Он устал за день как пес, выдержал довольно нервное согласование окончательного варианта операции и даже успел оказать первую медицинскую помощь одному из аналитиков СИБ, посмевшему поинтересоваться пренебрежительно в стиле «А эта что тут делает вообще⁈
- current normalized: Он устал за день как пес, выдержал довольно нервное согласование окончательного варианта операции и даже успел оказать первую медицинскую помощь одному из аналитиков СИБ, посмевшему поинтересоваться пренебрежительно в стиле «А эта что тут делает вообще?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0094 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А без пропуска все едино — не пущу!
- current normalized: А без пропуска все едино — не пущу!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0097 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Да они все тут с ума посходили!
- current normalized: «Да они вс+е тут с ума посходили!
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0097 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Тот округлили глаза и покачал головой.
- current normalized: Тот округлили глаза и покачал головой.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0104 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Бронежилеты скрытого ношения, амулеты, и вот это вот все…
- current normalized: — Бронежилеты скрытого ношения, амулеты, и вот это вот все…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0106 / `Ну-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну-у-у-у…
- current normalized: — Нууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0108 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Павел все это время тренировал самую невинную улыбку, на какую только был способен.
- current normalized: Павел всё это время тренировал самую невинную улыбку, на какую только был способен.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0108 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Нет, сторонний наблюдатель, может, и впечатлился бы, да только сестренке, краем глаза наблюдавшей за стараниями молодого человека, казалось, что у него разом заболели все зубы.
- current normalized: Нет, сторонний наблюдатель, может, и впечатлился бы, да только сестренке, краем глаза наблюдавшей за стараниями молодого человека, казалось, что у него разом заболели все зубы.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0108 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Нет, сторонний наблюдатель, может, и впечатлился бы, да только сестренке, краем глаза наблюдавшей за стараниями молодого человека, казалось, что у него разом заболели все зубы.
- current normalized: Нет, сторонний наблюдатель, может, и впечатлился бы, да только сестренке, краем глаза наблюдавшей за стараниями молодого человека, казалось, что у него разом заболели все зубы.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0109 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — Я жду ответа, — строго напомнила о себе девушка, сделав шаг к сотруднице СИБ.
- current normalized: — Я жду ответа, — строго напомнила о себе девушка, сделав шаг к сотруднице СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0131 / `йо-о-о-о`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Уй-йо-о-о-о…
- current normalized: — Уй-йооо…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0134 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Хватило и закапанного пола, чтобы у местной «фрейлины» глаза налились кровью.
- current normalized: Хватило и закапанного пола, чтобы у местной «фрейлины» глаза налились кровью.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0139 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Во всяком случае, она оказалась куда умнее своей подчиненной, а потому сразу же приняла из рук Светланы бланк приказа за подписью представителя СИБ в учебном заведении.
- current normalized: Во всяком случае, она оказалась куда умнее своей подчиненной, а потому сразу же приняла из рук Светланы бланк приказа за подписью представителя СИБ в учебном заведении.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0146 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все в порядке, я понимаю.
- current normalized: — Все в порядке, я понимаю.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0160 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако к двери все-таки направилась.
- current normalized: Однако к двери всё-таки направилась.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0164 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза урожденной Юсуповой мгновенно распахнулись.
- current normalized: Глаза урожденной Юсуповой мгновенно распахнулись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0168 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В конце концов, все это оплачивать приходилось именно клановцу.
- current normalized: В конце концов, всё это оплачивать приходилось именно клановцу.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0168 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все же…
- current normalized: Но всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0171 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Практически все свободны, — ровно ответила девушка.
- current normalized: — Практически все свободны, — ровно ответила девушка.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0180 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Это все он, — ткнула клановка пальцем в брата.
- current normalized: — Это все он, — ткнула кл+ановка пальцем в брата.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0184 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки воспитанники Бойцова прекрасно представляли, как бы отреагировал инструктор, стоило бы кому-то из них НАСТОЛЬКО ошибиться.
- current normalized: Всё-таки воспитанники Бойцова прекрасно представляли, как бы отреагировал инструктор, стоило бы кому-то из них НАСТОЛЬКО ошибиться.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0190 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки сказки — штука такая.
- current normalized: Всё-таки сказки — штука такая.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0192 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки клановые традиции и не такое предполагают.
- current normalized: Всё-таки клановые традиции и не такое предполагают.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0200 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: Тон, интонация, нежность в глазах — идеально подобранные компоненты, чтобы растопить даже самое черствое сердце.
- current normalized: Тон, интонация, нежность в глазах — идеально подобранные компоненты, чтобы растопить даже самое черствое сердце.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0202 / `Ну-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну-у-у-у…
- current normalized: — Нууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0019-p-0203 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Он уже все решил, — с деланым отвращением в голосе припечатала Волконская, но тут же «похвасталась».
- current normalized: — Он уже все решил, — с деланым отвращением в голосе припечатала Волконская, но тут же «похвасталась».
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0007 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: Столько десятилетий благоверный фактически не видел семьи с высоты Трона, и вот, наконец, едва Демид получил возможность проводить время с ней, как появляются «эти».
- current normalized: Столько десятилетий благоверный фактически не видел семьи с высоты Трона, и вот, наконец, едва Демид получил возможность проводить время с ней, как появляются «эти».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0009 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Краем глаза мужчина отметил, что охрана не спит.
- current normalized: Краем глаза мужчина отметил, что охрана не спит.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0013 / `никого не было`
- class: не было; verdict: **OK**
- FB2 sentence: — Проводите ко мне, — негромко произнес он, вполне уверенный, что его услышат даже с учетом того, что поблизости никого не было.
- current normalized: — Проводите ко мне, — негромко произнес он, вполне уверенный, что его услышат даже с учетом того, что поблизости никого н+е было.
- current rule: `phrase.ne_bylo`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0019 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: — Не подумай, Костя, что я рад тебя видеть, — улыбнулся без капли веселости в глазах Демид Николаевич.
- current normalized: — Не подумай, Костя, что я рад тебя видеть, — улыбнулся без капли веселости в глазах Демид Николаевич.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0022 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Гость прекрасно помнил, что хозяин дома все эти кружева словесные, принятые в высшем обществе, терпеть не мог, отличаясь порой граничащей с хамством прямолинейность.
- current normalized: Гость прекрасно помнил, что хозяин дома все эти кружева словесные, принятые в высшем обществе, терпеть не мог, отличаясь порой граничащей с хамством прямолинейность.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0025 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все равно как если бы Гитлер, пытался требовать перемирия в 1945 году, когда советские войска уже вовсю штурмовали пригороды Берлина.
- current normalized: Всё равно как если бы Гитлер, пытался требовать перемирия в 1945 году, когда советские войска уже вовсю штурмовали пригороды Берлина.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0026 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Впрочем, у разведчика все было еще не настолько плохо.
- current normalized: Впрочем, у разведчика все было еще не настолько плохо.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0026 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Вот только их становилось все меньше.
- current normalized: Вот только их становилось всё меньше.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0030 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако Константин Ильич действительно оказался в тупике, а потому был готов выложить на сукно игрального стола вообще все, чтобы «наскрести» на ставку.
- current normalized: Однако Константин Ильич действительно оказался в тупике, а потому был готов выложить на сукно игрального стола вообще все, чтобы «наскрести» на ставку.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0030 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А там уж либо пан, либо все плохо.
- current normalized: А там уж либо пан, либо все плохо.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0035 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все столь же ровно поинтересовался Демид Николаевич, вновь берясь за крынку.
- current normalized: — все столь же ровно поинтересовался Демид Николаевич, вновь берясь за крынку.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0042 / `высоте`
- class: высоты; verdict: **OK**
- FB2 sentence: На стороне разведчика было преимущество в высоте.
- current normalized: На стороне разведчика было преимущество в высоте.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0049 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все мечтает, что их ветвь Трон займет.
- current normalized: Все мечтает, что их ветвь Трон займет.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0056 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А все потому, что их босс был просто в ярости.
- current normalized: А все потому, что их босс был просто в ярости.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0058 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Нет, даже его эмоции все же «сковырнут» птичку на землю, то он-то, скорее всего, выживет.
- current normalized: Нет, даже его эмоции всё же «сковырнут» птичку на землю, то он-то, скорее всего, выживет.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0070 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Однако если ты берешься угрожать самым близким для него людям, то далеко не всегда удается потом «извиниться» материальной компенсацией.
- current normalized: Однако если ты берешься угрожать самым близким для него людям, то далеко не всегда удается потом «извиниться» материальной компенсацией.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0072 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Чтобы обдумать все и вся, у Саши Мышкиной ушла целая неделя.
- current normalized: Чтобы обдумать все и вся, у Саши Мышкиной ушла целая неделя.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0085 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: Как-то требовательно, но в то же время с легкой насмешкой в глазах.
- current normalized: Как-то требовательно, но в то же время с легкой насмешкой в глазах.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0090 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Кофе, стакан воды — вот и все, что ему было нужно для короткой беседы.
- current normalized: Кофе, стакан воды — вот и все, что ему было нужно для короткой беседы.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0095 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако с момента происшествия прошло уже достаточно, а Рина все еще общалась с читателями в блогах и даже по видеосвязи.
- current normalized: Однако с момента происшествия прошло уже достаточно, а Рина всё еще общалась с читателями в блогах и даже по видеосвязи.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0104 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В этих влажных фантазиях, помноженных на страх и желание отыграться за прошлые встречи, все было как-то проще.
- current normalized: В этих влажных фантазиях, помноженных на страх и желание отыграться за прошлые встречи, все было как-то проще.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0107 / `ма-а-а-аленький`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Стоит также упомянуть ма-а-а-аленький нюанс: девушка действительно была должна Павлу.
- current normalized: Стоит также упомянуть маааленький нюанс: девушка действительно была должна Павлу.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0109 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако ему было все равно.
- current normalized: Однако ему было всё равно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0114 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Имена были действительно все.
- current normalized: Имена были действительно все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0114 / `ВСЕ`
- class: все/всё; verdict: **OK**
- FB2 sentence: И не только в рамках этого дела, а вообще ВСЕ.
- current normalized: И не только в рамках этого дела, а вообще ВСЕ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0116 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — СИБ, — пожал плечами Павел.
- current normalized: — СИБ, — пожал плечами Павел.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0125 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все же занервничала.
- current normalized: Но всё же занервничала.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0125 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: СИБ и канцелярия — вовсе не шутки!
- current normalized: СИБ и канцелярия — вовсе не шутки!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0130 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А это значит, что все вопросы, связанные с каждым из Мышкиных канцелярия, держит на контроле.
- current normalized: А это значит, что все вопросы, связанные с каждым из Мышкиных канцелярия, держит на контроле.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0130 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Ну а СИБ…
- current normalized: Ну а СИБ…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0132 / `ма-а-а-аленький`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Это я молчу про тот ма-а-а-аленький фактик, что в корпоративной среде о-о-очень не любят тех, кто привлекает государство к решению «внутренних» вопросов.
- current normalized: Это я молчу про тот маааленький фактик, что в корпоративной среде ооочень не любят тех, кто привлекает государство к решению «внутренних» вопросов.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0132 / `о-о-очень`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Это я молчу про тот ма-а-а-аленький фактик, что в корпоративной среде о-о-очень не любят тех, кто привлекает государство к решению «внутренних» вопросов.
- current normalized: Это я молчу про тот маааленький фактик, что в корпоративной среде ооочень не любят тех, кто привлекает государство к решению «внутренних» вопросов.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0146 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Вы все врешь!
- current normalized: — Вы все врешь!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0150 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Этот урок собеседнице он решил все же преподать.
- current normalized: Этот урок собеседнице он решил всё же преподать.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0150 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Конечно, все это имеет смысл, если журналистка вывернется из сегодняшней ситуации.
- current normalized: Конечно, всё это имеет смысл, если журналистка вывернется из сегодняшней ситуации.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0151 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Волконскому вовсе не хотелось, чтобы все закончилось слишком быстро и уж тем более фатально.
- current normalized: Волконскому вовсе не хотелось, чтобы все закончилось слишком быстро и уж тем более фатально.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0152 / `Фамилиии`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Доставшийся от матушки темперамент буквально сжигал изнутри, требуя поставить «этого мужлана» на место невзирая ни на какие Фамилиии.
- current normalized: Доставшийся от матушки темперамент буквально сжигал изнутри, требуя поставить «этого мужлана» на место невзирая ни на какие Фамилиии.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0157 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: Вот только «снаряд» разлетелся о противоположную стену.
- current normalized: Вот только «снаряд» разлетелся о противоположную стену.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0158 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Он закашлялся и совершенно не успел поймать миг, когда для него все кончилось.
- current normalized: Он закашлялся и совершенно не успел поймать миг, когда для него все кончилось.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0165 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: зажмурила глаза.
- current normalized: зажмурила глаза.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0166 / `Глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: — Глазки открой!
- current normalized: — Глазки открой!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0020-p-0168 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Ну, вот и все, — хмыкнул тот, ничуть не смущаясь.
- current normalized: — Ну, вот и все, — хмыкнул тот, ничуть не смущаясь.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0009 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А началось все с холодного властного голоса, как говаривали в старину, «в трубке»:
- current normalized: А началось все с холодного властного голоса, как говаривали в старину, «в трубке»:
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0011 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Тратить драгоценные мгновения на то, чтобы выслушать собеседника или хотя бы убедиться, что он все услышал и понял, никто не стал.
- current normalized: Тратить драгоценные мгновения на то, чтобы выслушать собеседника или хотя бы убедиться, что он все услышал и понял, никто не стал.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0013 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки хронический стресс под давлением окружающей среды — штука очень разрушительная.
- current normalized: Всё-таки хронический стресс под давлением окружающей среды — штука очень разрушительная.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0014 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: А потом прозвучал звонок.
- current normalized: А пот+ом прозвучал звонок.
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0016 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: Глеб Борисович Архипов властью обладал немалой.
- current normalized: Глеб Борисович Архипов властью обладал немалой.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0022 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все убранство было лаконично, монументально и очень-очень дорого.
- current normalized: Все убранство было лаконично, монументально и очень-очень дорого.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0022 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Образ подчеркивал просто, но явно сшитый на заказ костюм и то самое «каменное» выражение лица.
- current normalized: Образ подчеркивал просто, но явно сшитый на заказ костюм и то самое «каменное» выражение лица.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0023 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Садитесь, — ровно то ли приказал, то ли предложил Глеб Борисович, кивнув на кресло для посетителей.
- current normalized: — Садитесь, — ровно то ли приказал, то ли предложил Глеб Борисович, кивнув на кресло для посетителей.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0029 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Глеб Борисович, все это время посвятивший работе с документами на столе, дал возможность посетителю все ми гранями ужаса, после чего медленно поднял равнодушный взгляд и, подпустив лишь самую малую толику презрения в голос, заключил.
- current normalized: Глеб Борисович, всё это время посвятивший работе с документами на столе, дал возможность посетителю все ми гранями ужаса, после чего медленно поднял равнодушный взгляд и, подпустив лишь самую малую толику презрения в голос, заключил.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0029 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Глеб Борисович, все это время посвятивший работе с документами на столе, дал возможность посетителю все ми гранями ужаса, после чего медленно поднял равнодушный взгляд и, подпустив лишь самую малую толику презрения в голос, заключил.
- current normalized: Глеб Борисович, всё это время посвятивший работе с документами на столе, дал возможность посетителю все ми гранями ужаса, после чего медленно поднял равнодушный взгляд и, подпустив лишь самую малую толику презрения в голос, заключил.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0029 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: Глеб Борисович, все это время посвятивший работе с документами на столе, дал возможность посетителю все ми гранями ужаса, после чего медленно поднял равнодушный взгляд и, подпустив лишь самую малую толику презрения в голос, заключил.
- current normalized: Глеб Борисович, всё это время посвятивший работе с документами на столе, дал возможность посетителю все ми гранями ужаса, после чего медленно поднял равнодушный взгляд и, подпустив лишь самую малую толику презрения в голос, заключил.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0036 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все дело было в комме, мирно покоившимся на дне внутреннего кармана пиджака.
- current normalized: Все дело было в комме, мирно покоившимся на дне внутреннего кармана пиджака.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0052 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мол, почти дотянулись, но все равно вырваться из статуса «червей» пока не удалось.
- current normalized: Мол, почти дотянулись, но всё равно вырваться из статуса «червей» пока не удалось.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0054 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Пьяный в умат он орал что-то про «пропади оно все пропадом», не забывая прикладываться к бутылке явно дешевого пойла.
- current normalized: Пьяный в умат он орал что-то про «пропади оно все пропадом», не забывая прикладываться к бутылке явно дешевого пойла.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0055 / `А-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — А-а-а-а…
- current normalized: — ААА…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Эффект превзошел все ожидания.
- current normalized: Эффект превзошел все ожидания.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0070 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: С неотвратимостью покинувшей шахту ракеты он поднялся и все больше набирая скорость, рванул к одной из ванных комнат.
- current normalized: С неотвратимостью покинувшей шахту ракеты он поднялся и всё больше набирая скорость, рванул к одной из ванных комнат.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0071 / `Бу-э-э-э-э`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Бу-э-э-э-э!..
- current normalized: — Буэээ!..
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0074 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все остальные свободны.
- current normalized: Все остальные свободны.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0084 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все настолько плохо?
- current normalized: — Все настолько плохо?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0097 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Но потом сжечь!
- current normalized: Но потом сжечь!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0097 / `Ну-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Ну-у-у-у, она же красивая…
- current normalized: Нууу, она же красивая…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0098 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Утро субботы встретило Павла ярким солнышком, бьющим прямо в глаза, запахом сырников, и едва слышным посапыванием Елены Кошкиной.
- current normalized: Утро субботы встретило Павла ярким солнышком, бьющим прямо в глаза, запахом сырников, и едва слышным посапыванием Елены Кошкиной.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0098 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Впрочем, стоило только Волконскому пошевелиться, как девушка моментально проснулась и хитрющими глазами уставилась на молодого человека.
- current normalized: Впрочем, стоило только Волконскому пошевелиться, как девушка моментально проснулась и хитрющими глазами уставилась на молодого человека.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0100 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А эксперименты Виктории с каждым разом становились все более успешными.
- current normalized: А эксперименты Виктории с каждым разом становились все более успешными.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0112 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Волконский почувствовал, как у него холодеет в груди, краем глаза отмечая чуть бледное лицо едва ли не вытянувшейся по стойке «Смирно!
- current normalized: Волконский почувствовал, как у него холодеет в груди, краем глаза отмечая чуть бледное лицо едва ли не вытянувшейся по стойке «Смирно!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0116 / `Э-э-э-э-эй`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Э-э-э-э-эй!
- current normalized: — ЭЭЭй!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0123 / `Не-е-е-е`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Не-е-е-е, — протянула Кошкина, окинув шутливо-насмешливым взглядом «гостя».
- current normalized: — Неее, — протянула Кошкина, окинув шутливо-насмешливым взглядом «гостя».
- current rule: `lexicon.project, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0130 / `Све-е-е-ета`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Све-е-е-ета!
- current normalized: — Свееета!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0131 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Волконский на миг прикрыл глаза.
- current normalized: Волконский на миг прикрыл глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0132 / `привее-е-е-е-е-е`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Всем привее-е-е-е-е-е…
- current normalized: — Всем привеее…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0132 / `А-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — А-а-а-а?..
- current normalized: Кхм.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0135 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Отца сегодняшнего гостя в лицо знали все абсолютно.
- current normalized: Отца сегодняшнего гостя в лицо знали все абсолютно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0021-p-0135 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А вот с сыном было все несколько сложнее.
- current normalized: А вот с сыном было все несколько сложнее.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0002 / `стене`
- class: стены; verdict: **OK**
- FB2 sentence: Павел сидел на кровати, уставившись в одну точку на стене.
- current normalized: Павел сидел на кровати, уставившись в одну точку на стене.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0004 / `Фу-у-у-ух`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Фу-у-у-ух, — протяжно выдохнул Волконский, первым сбрасывая странное оцепенение.
- current normalized: — Фууух, — протяжно выдохнул Волконский, первым сбрасывая странное оцепенение.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Светлана — все еще в стену.
- current normalized: Светлана — всё еще в стену.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0008 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: Светлана — все еще в стену.
- current normalized: Светлана — всё еще в стену.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0011 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все, казалось бы, так просто, без подвоха.
- current normalized: И все, казалось бы, так просто, без подвоха.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0012 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все также безжизненно выдавил из себя Павел.
- current normalized: — все также безжизненно выдавил из себя Павел.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0015 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Волконский согласно качнул головой, краем глаза замечая за спиной Виктории знакомые кудри и блеск линз очков.
- current normalized: Волконский согласно качнул головой, краем глаза замечая за спиной Виктории знакомые кудри и блеск линз очков.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0017 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В отличие от парней, все еще наслаждающихся сырниками, Лена оценила реакцию «небожителей» и Катерины на мгновенно расположившего к себе всех остальных гостя.
- current normalized: В отличие от парней, всё еще наслаждающихся сырниками, Лена оценила реакцию «небожителей» и Катерины на мгновенно расположившего к себе всех остальных гостя.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0021 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В сей замечательный миг ей было абсолютно все равно на свой образ Ледяной королевы.
- current normalized: В сей замечательный миг ей было абсолютно всё равно на свой образ Ледяной королевы.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0022 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Либо ответь, пожалуйста, по существу, либо скажи, что мне знать этого не положено, и я отправлюсь есть сырники, пока Ирка с парнями все не слопала.
- current normalized: Либо ответь, пожалуйста, по существу, либо скажи, что мне знать этого не положено, и я отправлюсь есть сырники, пока Ирка с парнями все не слопала.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0026 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: По мере понимания лицо девушки все больше краснело, а в глазах все отчетливее становилась видна паника.
- current normalized: По мере понимания лицо девушки всё больше краснело, а в глазах все отчетливее становилась видна паника.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0026 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: По мере понимания лицо девушки все больше краснело, а в глазах все отчетливее становилась видна паника.
- current normalized: По мере понимания лицо девушки всё больше краснело, а в глазах все отчетливее становилась видна паника.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0026 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: По мере понимания лицо девушки все больше краснело, а в глазах все отчетливее становилась видна паника.
- current normalized: По мере понимания лицо девушки всё больше краснело, а в глазах все отчетливее становилась видна паника.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0063 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — поинтересовался отец, задумчиво наблюдая за тем, как Федор самолично заправляет древний, дубовый, но все еще безотказно надежный внедорожник.
- current normalized: — поинтересовался отец, задумчиво наблюдая за тем, как Федор самолично заправляет древний, дубовый, но всё еще безотказно надежный внедорожник.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0073 / `Фу-у-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Фу-у-у-у-у!
- current normalized: — Фууу!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0078 / `стеной`
- class: стены; verdict: **OK**
- FB2 sentence: — Не нравится мне это, — коротко объявил Федор, имея в виду крупные хлопья снега, валящиеся на землю сплошной стеной.
- current normalized: — Не нравится мне это, — коротко объявил Федор, имея в виду крупные хлопья снега, валящиеся на землю сплошной стеной.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0079 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но с другой все эти Волконские-Юсуповы-Архиповы будут совершенно неважны, если они сейчас встретятся лоб в лоб с «ослепшим» большегрузом.
- current normalized: Но с другой все эти Волконские-Юсуповы-Архиповы будут совершенно неважны, если они сейчас встретятся лоб в лоб с «ослепшим» большегрузом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0083 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако занять небольшой удалённый столик в уголке им все же удалось.
- current normalized: Однако занять небольшой удалённый столик в уголке им всё же удалось.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0090 / `Потом`
- class: потом; verdict: **OK**
- FB2 sentence: — Потом вернешься к работе.
- current normalized: — Потом вернешься к работе.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0095 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Но потом будь готова к работе!
- current normalized: Но потом будь готова к работе!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0107 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако в этом красноречивом безмолвии легко угадывалось все, что он хотел бы сказать сейчас.
- current normalized: Однако в этом красноречивом безмолвии легко угадывалось все, что он хотел бы сказать сейчас.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0113 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — И что все это значит?
- current normalized: — И что всё это значит?
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0117 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако все лимиты были выбраны.
- current normalized: Однако все лимиты были выбраны.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0119 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Правда, все больше в «тепличных» и ограниченных множеством условий клановых войнах, а не, например, в Ханьской мясорубке.
- current normalized: Правда, всё больше в «тепличных» и ограниченных множеством условий клановых войнах, а не, например, в Ханьской мясорубке.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0119 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все же…
- current normalized: Но всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0122 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Приложим все усилия.
- current normalized: — Приложим все усилия.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0133 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Сделай все так, чтобы вина падала на Волконских!
- current normalized: — Сделай все так, чтобы вина падала на Волконских!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0134 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки крепкие спиртные напитки в клановой среде были не очень распространены, а потому не всякий носитель Фамилии умел пить.
- current normalized: Всё-таки крепкие спиртные напитки в клановой среде были не очень распространены, а потому не всякий носитель Фамилии умел пить.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0145 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: В глазах молодой красноволосой девицы в фирменном передничке мелькнуло сочувствие.
- current normalized: В глазах молодой красноволосой девицы в фирменном передничке мелькнуло сочувствие.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0147 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Даже позволил себе встать и, не без некоторого труда, но все же вполне уверенно, шутовски раскланяться.
- current normalized: Даже позволил себе встать и, не без некоторого труда, но всё же вполне уверенно, шутовски раскланяться.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0147 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мол, в другой раз и все такое прочее.
- current normalized: Мол, в другой раз и все такое прочее.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0148 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все же…
- current normalized: Но всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0154 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза ее чуть удивленно распахнулись.
- current normalized: Глаза ее чуть удивленно распахнулись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0155 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: — Сильный, — коротко охарактеризовала девочка, вдруг замерев и прищурив серьезные глазки.
- current normalized: — Сильный, — коротко охарактеризовала девочка, вдруг замерев и прищурив серьезные глазки.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0160 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: На глаза ей тут же попалась зеркальная стена кафе, в отражении которой прекрасно было видно входную группу…
- current normalized: На глаза ей тут же попалась зеркальная стена кафе, в отражении которой прекрасно было видно входную группу…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0160 / `стена`
- class: стены; verdict: **OK**
- FB2 sentence: На глаза ей тут же попалась зеркальная стена кафе, в отражении которой прекрасно было видно входную группу…
- current normalized: На глаза ей тут же попалась зеркальная стена кафе, в отражении которой прекрасно было видно входную группу…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0163 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все притихли.
- current normalized: Вс+е притихли.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0163 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Храни нас пуще всех печалей и все такое прочее!..
- current normalized: «Храни нас пуще всех печалей и все такое прочее!..
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0166 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Вот только стоило лишь мельком глянуть на то, какими глазами смотрела на гвардейца Вера, чтобы все стало понятно.
- current normalized: Вот только стоило лишь мельком глянуть на то, какими глазами смотрела на гвардейца Вера, чтобы все стало понятно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0166 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Вот только стоило лишь мельком глянуть на то, какими глазами смотрела на гвардейца Вера, чтобы все стало понятно.
- current normalized: Вот только стоило лишь мельком глянуть на то, какими глазами смотрела на гвардейца Вера, чтобы все стало понятно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0175 / `эта-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Че, эта-а-а-а…
- current normalized: — Че, этааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0178 / `Эта-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Эта-а-а-а…
- current normalized: — Этааа…
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0180 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Вы все врете!
- current normalized: — Вы все врете!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0181 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Почти все взгляды сошлись на ней.
- current normalized: Почти все взгляды сошлись на ней.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0181 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Но вот сама девочка впилась в Дон Жуана полными ужаса глазами.
- current normalized: Но вот сама девочка впилась в Дон Жуана полными ужаса глазами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0182 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — закричала она и действительно с силой зажмурила глаза, для верности прикрыв их ладонями.
- current normalized: — закричала она и действительно с силой зажмурила глаза, для верности прикрыв их ладонями.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0022-p-0184 / `глазом`
- class: глаза; verdict: **OK**
- FB2 sentence: К смельчаку тут же бросился ближайший боец, но уже через миг как-то неловко упал на пол с выбитым той самой ручкой глазом.
- current normalized: К смельчаку тут же бросился ближайший боец, но уже через миг как-то неловко упал на пол с выбитым той самой ручкой глазом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0002 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все хорошо, — негромко выдохнул молодой человек, аккуратно делая шаг в сторону Риммы.
- current normalized: — Все хорошо, — негромко выдохнул молодой человек, аккуратно делая шаг в сторону Риммы.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0002 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все закончилось.
- current normalized: — Все закончилось.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0005 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все произошло мгновенно.
- current normalized: Все произошло мгновенно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0005 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Однако едва на него бросился коллега «ограбленного» стрелка, парень больше не сомневался, вогнав добычу ему в глаз.
- current normalized: Однако едва на него бросился коллега «ограбленного» стрелка, парень больше не сомневался, вогнав добычу ему в глаз.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0005 / `стрелка`
- class: стрелку; verdict: **OK**
- FB2 sentence: Однако едва на него бросился коллега «ограбленного» стрелка, парень больше не сомневался, вогнав добычу ему в глаз.
- current normalized: Однако едва на него бросился коллега «ограбленного» стрелка, парень больше не сомневался, вогнав добычу ему в глаз.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0006 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все это Павел отметил на автомате, падая на землю.
- current normalized: Всё это Павел отметил на автомате, падая на землю.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0006 / `стрелка`
- class: стрелку; verdict: **OK**
- FB2 sentence: Тело мгновенно среагировало на рывок ограбленного стрелка.
- current normalized: Тело мгновенно среагировало на рывок ограбленного стрелка.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: все.
- current normalized: все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В смысле, вообще «все».
- current normalized: В смысле, вообще «все».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0009 / `йе-е-е-о-о-о`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Уй-йе-е-е-о-о-о…
- current normalized: — Уй-йеееооо…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0010 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Он уже хотел добавить кое-что еще, но вдруг буквально споткнулся о необычайно серьезный взгляд голубых детских глаз.
- current normalized: Он уже хотел добавить кое-что еще, но вдруг буквально споткнулся о необычайно серьезный взгляд голубых детских глаз.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — В кино все врут…
- current normalized: — В кино вс+е врут…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0016 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Посетители кафе просто застыли мышками и ждали, когда именно все это закончится.
- current normalized: Посетители кафе просто застыли мышками и ждали, когда именно всё это закончится.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0020 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Молодой человек мысленно вздохнул, краем глаза отмечая пару внедорожников, в визге сбрасывающие скорость возле заведения.
- current normalized: Молодой человек мысленно вздохнул, краем глаза отмечая пару внедорожников, в визге сбрасывающие скорость возле заведения.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0022 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Она вдруг поняла, что у нее все-таки есть шанс оплатить обучение в столичном императорском технологическом институте.
- current normalized: Она вдруг поняла, что у нее всё-таки есть шанс оплатить обучение в столичном императорском технологическом институте.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0023 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все хорошо, — негромко выдохнул молодой человек, аккуратно делая шаг в сторону Риммы.
- current normalized: — Все хорошо, — негромко выдохнул молодой человек, аккуратно делая шаг в сторону Риммы.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0023 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все закончилось.
- current normalized: — Все закончилось.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0025 / `Отпусти-и-и-и`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Отпусти-и-и-и!
- current normalized: — Отпустиии!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0031 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Для него все происходящее тоже по нервишкам ударило.
- current normalized: Для него все происходящее тоже по нервишкам ударило.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0035 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки судьбу свою люди строят сами.
- current normalized: Всё-таки судьбу свою люди строят сами.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Уже все закончилось.
- current normalized: Уже все закончилось.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 9 / ch-0023-p-0040 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Ну, тут все в порядке…
- current normalized: — Ну, тут все в порядке…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0004 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: Но вот с высоты сто пятидесятого этажа эта грань между днем и ночью была очень заметна.
- current normalized: Но вот с высоты сто пятидесятого этажа эта грань между днем и ночью была очень заметна.
- current rule: `none`
- approximate MP3: 29.01 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0022 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Будущий Глава откинулся на спинку кресла и, вглядевшись в глаза отца, покачал головой:
- current normalized: Будущий Глава откинулся на спинку кресла и, вглядевшись в глаза отца, покачал головой:
- current rule: `none`
- approximate MP3: 159.58 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0024 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — Ты отчеты СИБ и канцелярии изучил?
- current normalized: — Ты отчеты СИБ и канцелярии изучил?
- current rule: `none`
- approximate MP3: 174.08 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0026 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Во-вторых, и это куда важнее, обрати внимание, кто именно тебе прислал все материалы.
- current normalized: Во-втор+ых, и это куда важнее, обрати внимание, кто именно тебе прислал все материалы.
- current rule: `lexicon.project`
- approximate MP3: 188.59 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0031 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все же вышесказанное будет иметь значение в миг, когда начнет прорабатываться долгосрочная стратегия.
- current normalized: Всё же вышесказанное будет иметь значение в миг, когда начнет прорабатываться долгосрочная стратегия.
- current rule: `silero.preprocessing`
- approximate MP3: 224.86 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0033 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Более того, старого воина постигло бы разочарование, если бы Игнат бросил все силы на решение подброшенной ему задачки именно сейчас.
- current normalized: Более того, старого воина постигло бы разочарование, если бы Игнат бросил все силы на решение подброшенной ему задачки именно сейчас.
- current rule: `lexicon.project`
- approximate MP3: 239.36 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0045 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все остальные…
- current normalized: И все остальные…
- current rule: `none`
- approximate MP3: 326.4 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0048 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Отец рассказывает далеко не все.
- current normalized: Отец рассказывает далеко не все.
- current rule: `none`
- approximate MP3: 348.16 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0054 / `родов`
- class: родов; verdict: **OK**
- FB2 sentence: Ради интриги получить разрешение канцелярии на сближение родов и ВОТ ТАК о нем объявить…
- current normalized: Ради интриги получить разрешение канцелярии на сближение родов и ВОТ ТАК о нем объявить…
- current rule: `silero.preprocessing`
- approximate MP3: 391.68 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0001-p-0055 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Как он собирается все это воплотить в жизнь?
- current normalized: Как он собирается всё это воплотить в жизнь?
- current rule: `silero.preprocessing`
- approximate MP3: 398.94 s; clip: `/tmp/book09-10-forensic/clips/book10_001__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0005 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все казалось, что их заманивают в ловушку, чтобы потом захлопнуть западню…
- current normalized: Все казалось, что их заманивают в ловушку, чтобы потом захлопнуть западню…
- current rule: `none`
- approximate MP3: 36.27 s; clip: `/tmp/book09-10-forensic/clips/book10_002__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0005 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Все казалось, что их заманивают в ловушку, чтобы потом захлопнуть западню…
- current normalized: Все казалось, что их заманивают в ловушку, чтобы потом захлопнуть западню…
- current rule: `none`
- approximate MP3: 36.27 s; clip: `/tmp/book09-10-forensic/clips/book10_002__.mp3`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0007 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В тот час, когда отменить или перенести операцию было нельзя, они исчерпали все лимиты на разведку.
- current normalized: В тот час, когда отменить или перенести операцию было нельзя, они исчерпали все лимиты на разведку.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0016 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — Так ведь и СИБ никакого отношения не имеет к охране, — чуть рассеянно откликнулась Ольга, вновь утыкаясь в планшет.
- current normalized: — Так ведь и СИБ никакого отношения не имеет к охране, — чуть рассеянно откликнулась Ольга, вновь утыкаясь в планшет.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0034 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако для специалистов изыски ландшафтных магов все равно оставались «зеленкой».
- current normalized: Однако для специалистов изыски ландшафтных магов всё равно оставались «зеленкой».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0036 / `статью`
- class: статью; verdict: **OK**
- FB2 sentence: — негромко поддержала «уралочку» Светлана, с королевской статью повернув голову в сторону вновь уставившегося на кусочек помидора брата.
- current normalized: — негромко поддержала «уралочку» Светлана, с королевской ст+атью повернув голову в сторону вновь уставившегося на кусочек помидора брата.
- current rule: `phrase.royal_statyu`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0037 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Для удобства Волконский его на вилку наколол, да на уровень глаз поднял.
- current normalized: Для удобства Волконский его на вилку наколол, да на уровень глаз поднял.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0049 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — А тебя вообще все что не сырники — не интересует!
- current normalized: — А тебя вообще все что не сырники — не интересует!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0059 / `не с чем`
- class: не с чем; verdict: **OK**
- FB2 sentence: Да и спорить в целом было не с чем.
- current normalized: Да и спорить в целом было н+е с чем.
- current rule: `phrase.ne_s_chem`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0063 / `стрелки`
- class: стрелку; verdict: **OK**
- FB2 sentence: Куда больше его волновали стрелки собственных часов.
- current normalized: Куда больше его волновали стрелки собственных часов.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0071 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Просто следуй указаниям преподавателей, и все будет хорошо…
- current normalized: — Просто следуй указаниям преподавателей, и все будет хорошо…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0079 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки, Андрей — молодец.
- current normalized: Всё-таки, Андрей — молодец.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0002-p-0079 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: Клановец уважительно кивнул, рассматривая стеклянную «стену».
- current normalized: Клановец уважительно кивнул, рассматривая стеклянную «стену».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — сообщила Юсупова, решив, что на все семь бед нашла замечательный единственный ответ.
- current normalized: — сообщила Юсупова, решив, что на все семь бед нашла замечательный единственный ответ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0014 / `о-о-очень`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Есть так, — о-о-очень привычно ответила девушка, уже склонившись к консоли управления.
- current normalized: — Есть так, — ооочень привычно ответила девушка, уже склонившись к консоли управления.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0020 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ему и в голову не могло прийти, что все НАСТОЛЬКО плохо.
- current normalized: Ему и в голову не могло прийти, что все НАСТОЛЬКО плохо.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0029 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: На том и заглохла, бессмысленно лупая глазами…
- current normalized: На том и заглохла, бессмысленно лупая глазами…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0052 / `Была-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Была-а-а-а…
- current normalized: — Былааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0052 / `болела-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Я болела-а-а…
- current normalized: — Я болелааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0054 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Слушай Свету, и все будет…
- current normalized: Слушай Свету, и все будет…
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0056 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: — Я высоты боюсь!
- current normalized: — Я высот+ы боюсь!
- current rule: `phrase.vysoty`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0061 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: — с полными ужаса глазами прошептала Виктория.
- current normalized: — с полными ужаса глазами прошептала Виктория.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0069 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: Тенью метнувшись к шкафу, клановец перебросил через голову ремень пускового контейнера, и уже через несколько секунд в три толчка от стены оказался внизу.
- current normalized: Тенью метнувшись к шкафу, клановец перебросил через голову ремень пускового контейнера, и уже через несколько секунд в три толчка от стены оказался внизу.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0074 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все четверо диверсантов все еще находились в комнате Юсуповой, спокойно дожидаясь, пока стрелку не надоест развлекаться или у него не кончатся патроны.
- current normalized: Все четверо диверсантов всё еще находились в комнате Юсуповой, спокойно дожидаясь, пока стрелк+у не надоест развлекаться или у него не кончатся патроны.
- current rule: `phrase.strelku, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0074 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все четверо диверсантов все еще находились в комнате Юсуповой, спокойно дожидаясь, пока стрелку не надоест развлекаться или у него не кончатся патроны.
- current normalized: Все четверо диверсантов всё еще находились в комнате Юсуповой, спокойно дожидаясь, пока стрелк+у не надоест развлекаться или у него не кончатся патроны.
- current rule: `phrase.strelku, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0074 / `стрелку`
- class: стрелку; verdict: **OK**
- FB2 sentence: Все четверо диверсантов все еще находились в комнате Юсуповой, спокойно дожидаясь, пока стрелку не надоест развлекаться или у него не кончатся патроны.
- current normalized: Все четверо диверсантов всё еще находились в комнате Юсуповой, спокойно дожидаясь, пока стрелк+у не надоест развлекаться или у него не кончатся патроны.
- current rule: `phrase.strelku, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0078 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Хотя он и успел заметить, как во все стороны буквально «плеснули» кирпичные блоки, а «общежитие» обзавелось приличной чуть чадящей дырой в фасаде…
- current normalized: Хотя он и успел заметить, как во все стороны буквально «плеснули» кирпичные блоки, а «общежитие» обзавелось приличной чуть чадящей дырой в фасаде…
- current rule: `phrase.hlopok`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0003-p-0078 / `хлопок`
- class: хлопок; verdict: **OK**
- FB2 sentence: Лучше всего он запомнил хлопок вышибного заряда, отправившего реактивную гранату с термобарической «начинкой» в сторону окна.
- current normalized: Лучше всего он запомнил хлоп+ок вышибного заряда, отправившего реактивную гранату с термобарической «начинкой» в сторону окна.
- current rule: `phrase.hlopok`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0002 / `стен`
- class: стены; verdict: **OK**
- FB2 sentence: Простота и лаконичность прослеживались во всем: от выкрашенных бежевой краской казенного оттенка стен, до безликой ковровой дорожки, проложенной явно не красоты ради, в чтоб звук шагов из коридора не отвлекал местных обитателей от дел государевых.
- current normalized: Простота и лаконичность прослеживались во всем: от выкрашенных бежевой краской казенного оттенка стен, до безликой ковровой дорожки, проложенной явно не красоты ради, в чтоб звук шагов из коридора не отвлекал местных обитателей от дел государевых.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0003 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки род свою историю вел еще от Великого княжества Литовского, а в Бархатную книгу внесен был аж 1682 году.
- current normalized: Всё-таки род свою историю вел еще от Великого княжества Литовского, а в Бархатную книгу внесен был аж 1682 году.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И род пережил все: войны, мировые катаклизмы, Вторые Темные века…
- current normalized: И род пережил все: войны, мировые катаклизмы, Втор+ые Темные века…
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Где теперь все те, кто веков шесть назад шутили, что из десяти прогуливающихся по Невскому проспекту, хоть один Голицын да сыщется?
- current normalized: Где теперь все те, кто веков шесть назад шутили, что из десяти прогуливающихся по Невскому проспекту, хоть один Голицын да сыщется?
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0009 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: Мужчине даже пришлось напомнить, что в этих стенах в отношении него правило «когда пришел, тогда и счастье» не действует.
- current normalized: Мужчине даже пришлось напомнить, что в этих стенах в отношении него правило «когда пришел, тогда и счастье» не действует.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0010 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: Он и так был практически уверен, о чем именно пойдет речь в стенах этого кабинета.
- current normalized: Он и так был практически уверен, о чем именно пойдет речь в стенах этого кабинета.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0010 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Голицын развернулся к гостевым креслам и едва не скривился, увидев там представителя СИБ при Классах.
- current normalized: Голицын развернулся к гостевым креслам и едва не скривился, увидев там представителя СИБ при Классах.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0029 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: С этими словами хозяин кабинета сделал жест в сторону стены, где располагалась огромная видеопанель.
- current normalized: С этими словами хозяин кабинета сделал жест в сторону стен+ы, где располагалась огромная видеопанель.
- current rule: `phrase.steny`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0032 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: — вежливо поинтересовался цесаревич, глянув на Светлейшего князя добрыми-добрыми глазами…
- current normalized: — вежливо поинтересовался цесаревич, глянув на Светлейшего князя добрыми-добрыми глазами…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0036 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Представители СИБ не шелохнулись.
- current normalized: Представители СИБ не шелохнулись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0040 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все собравшиеся собственными глазами увидели, как на охраняемую территорию пробралась группа спецов с оружием и более чем внушительным боезапасом.
- current normalized: Все собравшиеся собственными глазами увидели, как на охраняемую территорию пробралась группа спецов с оружием и более чем внушительным боезапасом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0040 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Все собравшиеся собственными глазами увидели, как на охраняемую территорию пробралась группа спецов с оружием и более чем внушительным боезапасом.
- current normalized: Все собравшиеся собственными глазами увидели, как на охраняемую территорию пробралась группа спецов с оружием и более чем внушительным боезапасом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0042 / `нападавших`
- class: нападавших; verdict: **OK**
- FB2 sentence: Целых ЧЕТЫРЕ минуты ВСЕГО четверо нападавших, как на параде вышагивали ни от кого не скрываясь, лишь изредка постреливая по сторонам, чтобы расчистить себе дорогу.
- current normalized: Целых ЧЕТЫРЕ минуты ВСЕГО четверо напад+авших, как на параде вышагивали ни от кого не скрываясь, лишь изредка постреливая по сторонам, чтобы расчистить себе дорогу.
- current rule: `phrase.napadavshih`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0043 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Так вы все еще настаиваете, что буквальное соблюдение традиций стоит того, чтобы рисковать будущим государства.
- current normalized: Так вы всё еще настаиваете, что буквальное соблюдение традиций стоит того, чтобы рисковать будущим государства.
- current rule: `phrase.rodov, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0043 / `родов`
- class: родов; verdict: **OK**
- FB2 sentence: Напомню, что представители Великих родов несут службу в Дружине.
- current normalized: Напомню, что представители великих род+ов несут службу в Дружине.
- current rule: `phrase.rodov, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0043 / `родов`
- class: родов; verdict: **OK**
- FB2 sentence: Однако еще у пятидесяти шести кланов рангом пониже, ста восемнадцати родов и девяносто трех Семей может быть иное мнение.
- current normalized: Однако еще у пятидесяти шести кланов рангом пониже, ста восемнадцати родов и девяносто трех Семей может быть иное мнение.
- current rule: `phrase.rodov, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0053 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Хозяин кабинета глянул на представителя СИБ в Классах, а затем перевел взгляд на Седого Филина.
- current normalized: Хозяин кабинета глянул на представителя СИБ в Классах, а затем перевел взгляд на Седого Филина.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0058 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако все присутствующие предпочли сделать, вид, что государь многозначительно промолчал.
- current normalized: Однако все присутствующие предпочли сделать, вид, что государь многозначительно промолчал.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0060 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: После такого «отдыха» домой Павлу не хотелось, а потому он настоял, чтобы вся дружная компания отправилась на одну из резервных баз СИБ.
- current normalized: После такого «отдыха» домой Павлу не хотелось, а потому он настоял, чтобы вся дружная компания отправилась на одну из резервных баз СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0063 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: С другого бока тут же «подкатилась» Мышь, одарив клановца чистым, невинным взором голубых глаз и прекрасным видом на содержимое одного из своих любимых полупрозрачных топиков.
- current normalized: С другого бока тут же «подкатилась» Мышь, одарив клановца чистым, невинным взором голубых глаз и прекрасным видом на содержимое одного из своих любимых полупрозрачных топиков.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0072 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: А потому Павел, мысленно прикрыв глаза, протянул:
- current normalized: А потому Павел, мысленно прикрыв глаза, протянул:
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0004-p-0079 / `да-а-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — О да-а-а-а-а…
- current normalized: — О дааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0004 / `стрелка`
- class: стрелку; verdict: **OK**
- FB2 sentence: Тишь должна будет разместиться «за стрелка» на переднем пассажирском сидении.
- current normalized: Тишь должна будет разместиться «за стрелка» на переднем пассажирском сидении.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0019 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — У вас все готово?
- current normalized: — У вас все готово?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0025 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все по графику, — сухо бросил молодой человек.
- current normalized: — Все по графику, — сухо бросил молодой человек.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ой, все!
- current normalized: Ой, все!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0041 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Оттого-то и сосредоточил все свое внимание на «невесте» клановец.
- current normalized: Оттого-то и сосредоточил все свое внимание на «невесте» клановец.
- current rule: `lexicon.project, phrase.ne_bylo, phrase.litsa`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0041 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Судя по закаменевшим скулам и красноте лица, ему недоставало лишь пощады.
- current normalized: Судя по закаменевшим скулам и красноте лиц+а, ему недоставало лишь пощады.
- current rule: `lexicon.project, phrase.ne_bylo, phrase.litsa`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0041 / `вопросов не было`
- class: не было; verdict: **OK**
- FB2 sentence: Нет, к Максиму у него вопросов не было.
- current normalized: Нет, к Макс+иму у него вопросов н+е было.
- current rule: `lexicon.project, phrase.ne_bylo, phrase.litsa`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0053 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Павел, например, с интересом наблюдал за тем, как масочка возмущения и несправедливой обиды на весь женский род сползает с лица Максима, уступая место деловитой равнодушной сосредоточенности.
- current normalized: Павел, например, с интересом наблюдал за тем, как масочка возмущения и несправедливой обиды на весь женский род сползает с лица Макс+има, уступая место деловитой равнодушной сосредоточенности.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0056 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И молодой человек старался сделать все, чтобы судьба Юсуповой не стала причиной дописать еще пару строчек.
- current normalized: И молодой человек старался сделать все, чтобы судьба Юсуповой не стала причиной дописать еще пару строчек.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0056 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Во-вторых, пусть лучше у нее мозги встанут на место в столь «лайтовой» обстановки, чем потом «уралочка» погибнет просто от собственного несерьезного отношения к мерам безопасности.
- current normalized: Во-втор+ых, пусть лучше у нее мозги встанут на место в столь «лайтовой» обстановки, чем потом «уралочка» погибнет просто от собственного несерьезного отношения к мерам безопасности.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0058 / `меня-я-я-я`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Не начинайте без меня-я-я-я!!!
- current normalized: — Не начинайте без меняяя!!!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0060 / `не-е-е-ет`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Да не-е-е-ет…
- current normalized: — Да нееет…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0088 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все, ловушка захлопнулась.
- current normalized: Все, ловушка захлопнулась.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0005-p-0091 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все же я не считаю правильным присутствие Волконского в святая святых нашего клана.
- current normalized: — Всё же я не считаю правильным присутствие Волконского в святая святых нашего клана.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Хриплый голос оператора беспилотника звучал, как ему и было предписано инструкцией, сухо и деловито, однако едва слышное напряжение все же заставило Павла напрячься и глянуть в салонное зеркало заднего вида, чтобы оценить, как именно на эту новость отреагирует Тишь.
- current normalized: Хриплый голос оператора беспилотника звучал, как ему и было предписано инструкцией, сухо и деловито, однако едва слышное напряжение всё же заставило Павла напрячься и глянуть в салонное зеркало заднего вида, чтобы оценить, как именно на эту новость отреагирует Тишь.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0010 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Волконский и сам все слышал.
- current normalized: Волконский и сам все слышал.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0014 / `стрелковый`
- class: стрелку; verdict: **OK**
- FB2 sentence: — поинтересовался клановец, невольно поудобнее перехватывая компактный стрелковый комплекс.
- current normalized: — поинтересовался клановец, невольно поудобнее перехватывая компактный стрелковый комплекс.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0022 / `стрелков`
- class: стрелку; verdict: **OK**
- FB2 sentence: Аж на целых четырех стрелков.
- current normalized: Аж на целых четырех стрелков.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0023 / `стрелков`
- class: стрелку; verdict: **OK**
- FB2 sentence: — Занимаю второй ряд, — тут же констатировал Сергей не столько для пассажиров «Империала», сколько для водителей остальных стрелков.
- current normalized: — Занимаю втор+ой ряд, — тут же констатировал Сергей не столько для пассажиров «Империала», сколько для водителей остальных стрелков.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0031 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ну не палить же во все, что движется в самом центре столицы.
- current normalized: Ну не палить же во все, что движется в самом центре столицы.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0032 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все эти мысли никак не помешали клановцу поудобнее перекинуть ремень оружия через плечо и загнать патрон в ствол.
- current normalized: Все эти мысли никак не помешали клановцу поудобнее перекинуть ремень оружия через плечо и загнать патрон в ствол.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0034 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все в форме.
- current normalized: Все в форме.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0057 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: — только сейчас округлила глазки Юсупова.
- current normalized: — только сейчас округлила глазки Юсупова.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0066 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Не все были в «обвесе».
- current normalized: Не вс+е были в «обвесе».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0067 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — Обидно, да, — неловко крякнул Волконский, периферийным зрением наблюдая за тем, как в ужасе распахнулись глаза водителя «Ская», а сам он вскинул руки вверх.
- current normalized: — Обидно, да, — неловко крякнул Волконский, периферийным зрением наблюдая за тем, как в ужасе распахнулись глаза водителя «Ская», а сам он вскинул руки вверх.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0072 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Центр — Шуту, — раздался в наушнике все столь же невозмутимый голос оператора.
- current normalized: — Центр — Шуту, — раздался в наушнике все столь же невозмутимый голос оператора.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0080 / `Что-о-о-о`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: До обостренного до крайности слуха Волконского донеслось удивленно-протяжное «Что-о-о-о⁈
- current normalized: До обостренного до крайности слуха Волконского донеслось удивленно-протяжное «Чтооо?!
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0081 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Командир сводного отряда СИБ и клановой гвардии.
- current normalized: Командир сводного отряда СИБ и клановой гвардии.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0006-p-0087 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Вот и все отведенное время на разговоры.
- current normalized: Вот и все отведенное время на разговоры.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Он уже поставил все на зеро, и добавить сказанному было нечего.
- current normalized: Он уже поставил все на зеро, и добавить сказанному было нечего.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0004 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: » — мысленно улыбнулся воевода, все также умудрявшийся подпирать колонну с видом независимым и величественным.
- current normalized: » — мысленно улыбнулся воевода, все также умудрявшийся подпирать колонну с видом независимым и величественным.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0011 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все в зале об этом знали.
- current normalized: И все в зале об этом знали.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Сам же выступил на все деньги.
- current normalized: Сам же выступил на все деньги.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0016 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако общее настроение все равно неуловимо сместилось.
- current normalized: Однако общее настроение всё равно неуловимо сместилось.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0022 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Обвинение все-таки прозвучало.
- current normalized: Обвинение всё-таки прозвучало.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0026 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Ну вот и все!
- current normalized: «Ну вот и все!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0029 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: » — едва заметно покачал головой воевода, набивая короткое сообщение из трех слов: «Мы все оплатим!
- current normalized: » — едва заметно покачал головой воевода, набивая короткое сообщение из трех слов: «Мы все оплатим!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0032 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: » — тут же прозвучал в наушнике голос Бойцова, наблюдавшего за сценой с высоты птичьего полета «глазами» одного из беспилотников.
- current normalized: » — тут же прозвучал в наушнике голос Бойцова, наблюдавшего за сценой с высоты птичьего полета «глазами» одного из беспилотников.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0032 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: » — тут же прозвучал в наушнике голос Бойцова, наблюдавшего за сценой с высоты птичьего полета «глазами» одного из беспилотников.
- current normalized: » — тут же прозвучал в наушнике голос Бойцова, наблюдавшего за сценой с высоты птичьего полета «глазами» одного из беспилотников.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0034 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Куда больше парня интересовал невысокий лысый мужичок с добрыми глазами бывшего особиста в форме «Скорпионов», который тоже явно тянул время, рассчитывая на прибытие «официальных» гвардейцев.
- current normalized: Куда больше парня интересовал невысокий лысый мужичок с добрыми глазами бывшего особиста в форме «Скорпионов», который тоже явно тянул время, рассчитывая на прибытие «официальных» гвардейцев.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0035 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — За моей спиной Виктория Львовна Юсупова в окружении офицеров СИБ и клановых гвардейцев.
- current normalized: — За моей спиной Виктория Львовна Юсупова в окружении офицеров СИБ и клановых гвардейцев.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0044 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Кажется, кто-то все-таки догадался заткнуть ей рот.
- current normalized: Кажется, кто-то всё-таки догадался заткнуть ей рот.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0051 / `высоте`
- class: высоты; verdict: **OK**
- FB2 sentence: Идущая на сверхмалой высоте машина вынырнула из-за группы высоток, буквально протиснувшись между ними (ТАК «шутить» Волконский не решился бы никогда, но жизнь заставила!
- current normalized: Идущая на сверхмалой высоте машина вынырнула из-за группы высоток, буквально протиснувшись между ними (ТАК «шутить» Волконский не решился бы никогда, но жизнь заставила!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0051 / `высоток`
- class: высоты; verdict: **OK**
- FB2 sentence: Идущая на сверхмалой высоте машина вынырнула из-за группы высоток, буквально протиснувшись между ними (ТАК «шутить» Волконский не решился бы никогда, но жизнь заставила!
- current normalized: Идущая на сверхмалой высоте машина вынырнула из-за группы высоток, буквально протиснувшись между ними (ТАК «шутить» Волконский не решился бы никогда, но жизнь заставила!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0053 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: Остается только гадать, какие секретные разработки государевых лабораторий позволяют оператору «тяжа» чувствовать себе комфортно при падении с такой высоты.
- current normalized: Остается только гадать, какие секретные разработки государевых лабораторий позволяют оператору «тяжа» чувствовать себе комфортно при падении с такой высоты.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0054 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Какая-никакая, а все ж амортизация, да.
- current normalized: Какая-никакая, а всё ж амортизация, да.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0056 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Зоркий глаз наверняка бы заметил, что они немного отличаются от «знамени» основной ветви.
- current normalized: Зоркий глаз наверняка бы заметил, что они немного отличаются от «знамени» основной ветви.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0056 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Если Волконский настоящий, бойцы СИБ тоже (а кому еще будет дозволено владеть ТАКИМ оружием⁈
- current normalized: Если Волконский настоящий, бойцы СИБ тоже (а кому еще будет дозволено владеть ТАКИМ оружием?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0057 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако и тут лысый собеседник повел себя разумно, все больше разубеждая клановца в сходстве со своим «рекламным прототипом».
- current normalized: Однако и тут лысый собеседник повел себя разумно, всё больше разубеждая клановца в сходстве со своим «рекламным прототипом».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0072 / `стене`
- class: стены; verdict: **OK**
- FB2 sentence: — фыркнул себе под нос Павел, прижимаясь к стене таким образом, чтобы прямой выстрел из здания его не достал.
- current normalized: — фыркнул себе под нос Павел, прижимаясь к стене таким образом, чтобы прямой выстрел из здания его не достал.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0073 / `глазели`
- class: глаза; verdict: **OK**
- FB2 sentence: Да, люди останавливались, глазели на легендарных «тяжей».
- current normalized: Да, люди останавливались, глазели на легендарных «тяжей».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0083 / `стенка`
- class: стены; verdict: **OK**
- FB2 sentence: Естественно, стенка «пинка» не выдержала, провалившись внутрь.
- current normalized: Естественно, стенка «пинка» не выдержала, провалившись внутрь.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0007-p-0092 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Элитной и заоблачно дорогой, как и все здесь, но…
- current normalized: Элитной и заоблачно дорогой, как и все здесь, но…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0004 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все в порядке, Анна?
- current normalized: — Все в порядке, Анна?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0006 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все в порядки, Юлия Федоровна, — чуть поклонилась женщина.
- current normalized: — Все в порядки, Юлия Федоровна, — чуть поклонилась женщина.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0007 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А потому девушка слегка приподняла бровь, все-таки настаивая на ответе.
- current normalized: А потому девушка слегка приподняла бровь, всё-таки настаивая на ответе.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0017 / `стрелки`
- class: стрелку; verdict: **OK**
- FB2 sentence: Распахнулись створки «особого» элеватора, откуда тут же выскочил очень озабоченный мужчина лет тридцати в белой классической рубашке и темных брюках, о стрелки на которых можно было порезаться.
- current normalized: Распахнулись створки «особого» элеватора, откуда тут же выскочил очень озабоченный мужчина лет тридцати в белой классической рубашке и темных брюках, о стрелки на которых можно было порезаться.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0026 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все Юсуповы остаются на месте.
- current normalized: — Все Юсуповы остаются на месте.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0032 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Если тебя окружают плохие специалисты, то все главные ошибки в своей жизни ты уже совершил.
- current normalized: Если тебя окружают плохие специалисты, то все главные ошибки в своей жизни ты уже совершил.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Подскочившие гвардейцы сбили всех с троих с ног, тут же принявшись связывать разведчикам все доступные конечности.
- current normalized: Подскочившие гвардейцы сбили всех с троих с ног, тут же принявшись связывать разведчикам все доступные конечности.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0055 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: В какой-то момент его глаза натурально распахнулись в удивлении.
- current normalized: В какой-то момент его глаза натурально распахнулись в удивлении.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0058 / `стене`
- class: стены; verdict: **OK**
- FB2 sentence: Немедленно разворачивайте щит к той стене!
- current normalized: Немедленно разворачивайте щит к той стене!
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0059 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: Мол, хочет начальство от стены защищаться — кто ж ему злобный доктор-то⁈
- current normalized: Мол, хочет начальство от стены защищаться — кто ж ему злобный доктор-то?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0068 / `Юля-а-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Юля-а-а-а-а…
- current normalized: — Юляааа…
- current rule: `lexicon.project, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0069 / `Вито-о-о-ория`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Вито-о-о-ория-а-а-а-а-а Львовна-а-а-а-а…
- current normalized: — Витооорияааа Львовнааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0069 / `а-а-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Вито-о-о-ория-а-а-а-а-а Львовна-а-а-а-а…
- current normalized: — Витооорияааа Львовнааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0008-p-0069 / `Львовна-а-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Вито-о-о-ория-а-а-а-а-а Львовна-а-а-а-а…
- current normalized: — с трудом выдавила из себя та, попытавшись напомнить старшей подружке о клановом этикете.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0004 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все четко, выверено и лаконично.
- current normalized: Все четко, выверено и лаконично.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0004 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ведь все можно исправить.
- current normalized: Ведь все можно исправить.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0004 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Достаточно лишь выставить отсюда выскочку и убрать молокососа со сцены, а уж после решить все вопросы в узком семейном кругу.
- current normalized: Достаточно лишь выставить отсюда выскочку и убрать молокососа со сцены, а уж после решить все вопросы в узком семейном кругу.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0004 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Гордо возвышаясь над покинутым им креслом во весь невеликий рост, оратор сверкал глазами на предавших клановые идеалы родичей, допустивших «какого-то» Волконского в святая святых «уральцев».
- current normalized: Гордо возвышаясь над покинутым им креслом во весь невеликий рост, оратор сверкал глазами на предавших клановые идеалы родичей, допустивших «какого-то» Волконского в святая святых «уральцев».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0006 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Вот потом уже всех ждет нелегкое такое «слово за слово».
- current normalized: Вот потом уже всех ждет нелегкое такое «слово за слово».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0015 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — Согласен, — негромко ответил воевода, покосившись на штурмовую пару СИБ.
- current normalized: — Согласен, — негромко ответил воевода, покосившись на штурмовую пару СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0016 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Да и все «длинное» осталось за дверьми зала заседаний.
- current normalized: Да и все «длинное» осталось за дверьми зала заседаний.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0019 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Выкладывая исключительно факты, предоставленные СИБ и Волконским.
- current normalized: Выкладывая исключительно факты, предоставленные СИБ и Волконским.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0025 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Насколько мне известно, все исполнители погибли.
- current normalized: Насколько мне известно, вс+е исполнители погибли.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0030 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все головы в зале послушно обернулись к новой цели.
- current normalized: Все головы в зале послушно обернулись к новой цели.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0036 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: — Прекрасно, — лишь в этот миг Павел изволил «отлепиться» от стены.
- current normalized: — Прекрасно, — лишь в этот миг Павел изволил «отлепиться» от стены.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0048 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Тем более, если подходить с формальной точки зрения, оскорбление офицера СИБ и подозрение его в двурушничестве — оскорбление Короны.
- current normalized: Тем более, если подходить с формальной точки зрения, оскорбление офицера СИБ и подозрение его в двурушничестве — оскорбление Короны.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0055 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — В таком случае я прошу родичей разрешения предоставить трибуну Павлу Анатольевичу Волконскому и офицеру СИБ Валентине.
- current normalized: — В таком случае я прошу родичей разрешения предоставить трибуну Павлу Анатольевичу Волконскому и офицеру СИБ Валентине.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0065 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Я против, — заявил мужчина с таким видом, словно его мнение все еще интересовало хоть кого-то из присутствующих.
- current normalized: — Я против, — заявил мужчина с таким видом, словно его мнение всё еще интересовало хоть кого-то из присутствующих.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0073 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: даже если они приходят сквозь стены.
- current normalized: даже если они приходят сквозь стены.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0077 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Тревога подступала все ближе.
- current normalized: Тревога подступала всё ближе.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0079 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: Белокурое создание поклонилось и, похлопав очаровательными голубыми глазками, убежала за угощением для остальных.
- current normalized: Белокурое создание поклонилось и, похлопав очаровательными голубыми глазками, убежала за угощением для остальных.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0095 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Молодой человек искренне пожал плечами, краем глаза наблюдая за потоком мужчин и женщин, представлявших всю элиту Юсуповых, ныне стремящихся покинуть зал заседаний.
- current normalized: Молодой человек искренне пожал плечами, краем глаза наблюдая за потоком мужчин и женщин, представлявших всю элиту Юсуповых, ныне стремящихся покинуть зал заседаний.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0097 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Несколько секунд Лев Демидович всматривался в «послание», а потом ка-а-ак понял…
- current normalized: Несколько секунд Лев Дем+идович всматривался в «послание», а пот+ом кааак понял…
- current rule: `lexicon.project, phrase.potom, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0097 / `ка-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Несколько секунд Лев Демидович всматривался в «послание», а потом ка-а-ак понял…
- current normalized: Несколько секунд Лев Дем+идович всматривался в «послание», а пот+ом кааак понял…
- current rule: `lexicon.project, phrase.potom, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0009-p-0108 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Правда, под вопросительным взглядом сюзерена ему все равно пришлось ответить:
- current normalized: Правда, под вопросительным взглядом сюзерена ему всё равно пришлось ответить:
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0006 / `высоток`
- class: высоты; verdict: **OK**
- FB2 sentence: «Гарцующий» посреди городских высоток глайдер был заснят с самых разных ракурсов.
- current normalized: «Гарцующий» посреди городских высоток глайдер был заснят с самых разных ракурсов.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0011 / `высоте`
- class: высоты; verdict: **OK**
- FB2 sentence: Тем не менее мы видим глайдер с клановыми гербами в бесполетной зоне на «красной» высоте…
- current normalized: Тем не менее мы видим глайдер с клановыми гербами в бесполетной зоне на «красной» высоте…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0014 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: Даже глазки потупила.
- current normalized: Даже глазки потупила.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Внезапно Игорь Георгиевич на миг ощутил, насколько же ему все это надоело.
- current normalized: Внезапно Игорь Георгиевич на миг ощутил, насколько же ему всё это надоело.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0015 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Он, едва заметно хмыкнул и обвел глазами зал.
- current normalized: Он, едва заметно хмыкнул и обвел глазами зал.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0017 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако девушка все также продолжала упрямо пялиться в стол.
- current normalized: Однако девушка все также продолжала упрямо пялиться в стол.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0021 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Однако я все еще здесь, а не на приеме в Багряной палате…
- current normalized: — Однако я всё еще здесь, а не на приеме в Багряной палате…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0023 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Игорь Георгиевич развел руками и даже позволил себе скупую, но все же явную улыбку, чем пишущую братию поверг в самый натуральный шок.
- current normalized: — Игорь Георгиевич развел руками и даже позволил себе скупую, но всё же явную улыбку, чем пишущую братию поверг в самый натуральный шок.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0024 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Задавать уточняющие вопросы в стиле «Так все-таки вы утверждаете, что это не ваш глайдер?
- current normalized: Задавать уточняющие вопросы в стиле «Так всё-таки вы утверждаете, что это не ваш глайдер?
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0032 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Значит, разрешение на подобную операцию все-таки было?
- current normalized: Значит, разрешение на подобную операцию всё-таки было?
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0067 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Усталый, голодный (столовую в столичном управлении СИБ парень в последний раз посещал часов шесть назад, а перед отправкой домой не стал тратить время на очередной визит) и буквально выпотрошенный специалистами-мозгокрутами.
- current normalized: Усталый, голодный (столовую в столичном управлении СИБ парень в последний раз посещал часов шесть назад, а перед отправкой домой не стал тратить время на очередной визит) и буквально выпотрошенный специалистами-мозгокрутами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0092 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все прежние условия подтверждены.
- current normalized: — Все прежние условия подтверждены.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0096 / `Потом`
- class: потом; verdict: **OK**
- FB2 sentence: — Потом скинь посмотреть окончательный вариант договора.
- current normalized: — Потом скинь посмотреть окончательный вариант договора.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0100 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Одно дело допустить создание отдельного рода в клане, чтобы «когда-нибудь потом» формально спихнуть туда сверхперспективного аналитика и совершенно другое — сразу же одобрить его переход под «чужое крылышко».
- current normalized: Одно дело допустить создание отдельного рода в клане, чтобы «когда-нибудь потом» формально спихнуть туда сверхперспективного аналитика и совершенно другое — сразу же одобрить его переход под «чужое крылышко».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0102 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: С легким сердцем молодой человек завизировал «трансфер», и лишь потом спросил:
- current normalized: С легким сердцем молодой человек завизировал «трансфер», и лишь потом спросил:
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0104 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все еще Волконская, но уже не член правящей семьи, чуть виновато улыбнулась.
- current normalized: Всё еще Волконская, но уже не член правящей семьи, чуть виновато улыбнулась.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0115 / `Во-о-от`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Во-о-от…
- current normalized: — Вооот…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0118 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Волконский прикрыл глаза на миг.
- current normalized: Волконский прикрыл глаза на миг.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0126 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: — поразилась она, широко распахнув глазки.
- current normalized: — поразилась она, широко распахнув глазки.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0010-p-0128 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — воодушевилась девушка, предвкушая, чем все это может обернуться.
- current normalized: — воодушевилась девушка, предвкушая, чем всё это может обернуться.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако сердечко на какой-то миг все-таки екнуло и…
- current normalized: Однако сердечко на какой-то миг всё-таки екнуло и…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0008 / `Ну-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну-у-у-у…
- current normalized: — Нууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0012 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В смысле все целиком, а не определенными его частями.
- current normalized: В смысле все целиком, а не определенными его частями.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Во-первых, совсем скоро ему понадобятся все силы (хотя речь в первую очередь про душевные!
- current normalized: Во-первых, совсем скоро ему понадобятся все силы (хотя речь в первую очередь про душевные!
- current rule: `lexicon.project, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0015 / `мля-я-я-я-я`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: «Да мля-я-я-я-я…
- current normalized: «Да мляяя…
- current rule: `lexicon.project, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0019 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако и все на этом…
- current normalized: Однако и все на этом…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0024 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Мы не готовы все это потерять только потому, что ты мало уделяешь им…
- current normalized: — Мы не готовы всё это потерять только потому, что ты мало уделяешь им…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0028 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — справедливости ради все же заметила блондиночка.
- current normalized: — справедливости ради всё же заметила блондиночка.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0049 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: На секунду Кирилл замялся, но все же решился:
- current normalized: На секунду Кирилл замялся, но всё же решился:
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0050 / `Ка-а-ать`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ка-а-ать…
- current normalized: — Кааать…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0059 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако на этом все.
- current normalized: Однако на этом все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0066 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — От серьезной угрозы у нас все равно не хватит сил защититься, — продолжила Лена, и тут же с неким нездоровым цинизмом подмигнула.
- current normalized: — От серьезной угрозы у нас всё равно не хватит сил защититься, — продолжила Лена, и тут же с неким нездоровым цинизмом подмигнула.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0084 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все происходящее Евгению Драгунову перестало нравиться уже очень давно.
- current normalized: Все происходящее Евгению Драгунову перестало нравиться уже очень давно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0087 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки «золотая молодежь», как ни крути.
- current normalized: Всё-таки «золотая молодежь», как ни крути.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0089 / `глазу`
- class: глаза; verdict: **OK**
- FB2 sentence: Довольно разумная, тактичная, ну и глазу приятная, чего уж тут…
- current normalized: Довольно разумная, тактичная, ну и глазу приятная, чего уж тут…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0094 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако попытаться все же стоило.
- current normalized: Однако попытаться всё же стоило.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0104 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Та ответила спокойным взглядом безмятежных карих глаз.
- current normalized: Та ответила спокойным взглядом безмятежных карих глаз.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0108 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Да, ему все это не нравилось.
- current normalized: Да, ему всё это не нравилось.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0108 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но вознаграждение за такую работу искупало все…
- current normalized: Но вознаграждение за такую работу искупало все…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0123 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Объект он все равно уже упустил.
- current normalized: Объект он всё равно уже упустил.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0180 / `йяа-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Скотина, — глухо выдохнула Виктория, и тут же взмахнула плетью с диким криком «Ай-йяа-а-а-а!
- current normalized: — Скотина, — глухо выдохнула Виктория, и тут же взмахнула плетью с диким криком «Ай-йяааа!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0181 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Рвануло так, что ледяные осколки шрапнелью разлетелись во все стороны.
- current normalized: Рвануло так, что ледяные осколки шрапнелью разлетелись во все стороны.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0011-p-0197 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все.
- current normalized: И все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0003 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Потому она даже не попыталась выцарапать глаза Федору, когда он приехал за ней.
- current normalized: Потому она даже не попыталась выцарапать глаза Федору, когда он приехал за ней.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0006 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — С ним все в порядке, — ответил начальник охраны, не отводя взгляда от заметенной дороги.
- current normalized: — С ним все в порядке, — ответил начальник охраны, не отводя взгляда от заметенной дороги.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0009 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все остальное по остаточному принципу.
- current normalized: Всё остальное по остаточному принципу.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0013 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — завопила Мышкина во все горло.
- current normalized: — завопила Мышкина во все горло.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0013 / `А-а-а-а-а-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — А-а-а-а-а-а-а-а!!!
- current normalized: — ААА!!!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0030 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Девушка прикрыла глаза и откинулась на подголовник переднего пассажирского кресла внедорожника.
- current normalized: Девушка прикрыла глаза и откинулась на подголовник переднего пассажирского кресла внедорожника.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0031 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: все?
- current normalized: все?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако с каждым днем становилось все труднее.
- current normalized: Однако с каждым днем становилось все труднее.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И с каждым днем положение становилось все хуже.
- current normalized: И с каждым днем положение становилось всё хуже.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: все сильно плохо?
- current normalized: все сильно плохо?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0045 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Практически все.
- current normalized: Практически все.
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0045 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: А потом уезжать туда, где о них никто не знает.
- current normalized: А пот+ом уезжать туда, где о них никто не знает.
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0053 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А вот бутылку с собой все же прихватила.
- current normalized: А вот бутылку с собой всё же прихватила.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0065 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Для меня уже все…
- current normalized: — Для меня уже все…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0069 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: У нас все равно не хватит сил удержать компанию.
- current normalized: У нас всё равно не хватит сил удержать компанию.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0070 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все становилось понятно с самых первых слов.
- current normalized: Все становилось понятно с самых первых слов.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0082 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И, как бы все ни пошло, не вздумай высовываться.
- current normalized: И, как бы все ни пошло, не вздумай высовываться.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0086 / `ла-а-а-адно`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ой, да ла-а-а-адно, — разнесся от двери раздраженный голос.
- current normalized: — Ой, да лааадно, — разнесся от двери раздраженный голос.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0087 / `глазам`
- class: глаза; verdict: **OK**
- FB2 sentence: Судя по распахнувшимся глазам и остановившимся расширенным зрачкам, он тоже ощутил ЭТО.
- current normalized: Судя по распахнувшимся глазам и остановившимся расширенным зрачкам, он тоже ощутил ЭТО.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0088 / `здра-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Всем здра-а-а-а-сть, — зло выдохнул он.
- current normalized: — Всем здрааа-сть, — зло выдохнул он.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0090 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Гостья грациозным движением скинула капюшон, продемонстрировав красивое правильное лицо и блеск отсвечивающих Льдом глаз, после чего окинула помещение задумчивым взглядом, каким прораб оценивает фронт работ при сносе дома.
- current normalized: Гостья грациозным движением скинула капюшон, продемонстрировав красивое правильное лицо и блеск отсвечивающих Льдом глаз, после чего окинула помещение задумчивым взглядом, каким прораб оценивает фронт работ при сносе дома.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0092 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Так, — бодро объявил Волконский, плюхаясь все на тот же диван.
- current normalized: — Так, — бодро объявил Волконский, плюхаясь все на тот же диван.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0094 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Виктория Юсупова мягко шагнула вперед и, изящным движениям ухватив журналистку за подбородок, аккуратно подняла ее голову так, чтобы видеть глаза.
- current normalized: Виктория Юсупова мягко шагнула вперед и, изящным движениям ухватив журналистку за подбородок, аккуратно подняла ее голову так, чтобы видеть глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0097 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Эту статью Мышкина-Воробейчик написала еще лет в семнадцать, когда была молодой — глупой, и упивалась властью анонимно «выбрасывать в Сеть» все, что вздумается.
- current normalized: Эту статью Мышкина-Воробейчик написала еще лет в семнадцать, когда была молодой — глупой, и упивалась властью анонимно «выбрасывать в Сеть» все, что вздумается.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0097 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако Юсупова — это все равно что мифический «боксер», которого так просто обидеть, но практически невозможно успеть извиниться!
- current normalized: Однако Юсупова — это всё равно что мифический «боксер», которого так просто обидеть, но практически невозможно успеть извиниться!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0012-p-0097 / `статью`
- class: статью; verdict: **OK**
- FB2 sentence: Эту статью Мышкина-Воробейчик написала еще лет в семнадцать, когда была молодой — глупой, и упивалась властью анонимно «выбрасывать в Сеть» все, что вздумается.
- current normalized: Эту статью Мышкина-Воробейчик написала еще лет в семнадцать, когда была молодой — глупой, и упивалась властью анонимно «выбрасывать в Сеть» все, что вздумается.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0010 / `хлопок`
- class: хлопок; verdict: **OK**
- FB2 sentence: Просто раздался громкий хлопок, да жалобно звякнули стекла автомобиля.
- current normalized: Просто раздался громкий хлопок, да жалобно звякнули стекла автомобиля.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0011 / `ЧТО-О-О-О`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — ЧТО-О-О-О⁈
- current normalized: — ЧТООО?!
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0015 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Юрий Васильевич, хоть и отличившийся заметной бледностью лица, нашел в себе силы кивнуть.
- current normalized: Юрий Васильевич, хоть и отличившийся заметной бледностью лица, нашел в себе силы кивнуть.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0025 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Вообще-то, все должно было пройти куда спокойнее и…
- current normalized: Вообще-то, все должно было пройти куда спокойнее и…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0028 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Она ведь тоже так и не спросила ни разу, а куда именно все они так дружно едут на арендованной Волконским машине.
- current normalized: Она ведь тоже так и не спросила ни разу, а куда именно все они так дружно едут на арендованной Волконским машине.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0029 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Кстати, Клановец, отметивший краем глаза растрескавшееся лобовое стекло, отметил для себя две вещи: во-первых, он вовсе не зря взял машину на время (Кроль бы за такое обращение с его «Империалом» в глотку зубами вцепился!
- current normalized: Кстати, Клановец, отметивший краем глаза растрескавшееся лобовое стекло, отметил для себя две вещи: во-первых, он вовсе не зря взял машину на время (Кроль бы за такое обращение с его «Империалом» в глотку зубами вцепился!
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0030 / `Борисовича`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: Наберите, пожалуйста, Глеба Борисовича и назначьте встречу.
- current normalized: Наберите, пожалуйста, Глеба Борисовича и назначьте встречу.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0033 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все будет хорошо.
- current normalized: И все будет хорошо.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0038 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Здравствуйте, Глеб Борисович, — негромко произнес он.
- current normalized: — Здравствуйте, Глеб Борисович, — негромко произнес он.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0042 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все будет хорошо, Саш, — едва слышно шепнул отец, приобнимая девушку на встречу.
- current normalized: — Все будет хорошо, Саш, — едва слышно шепнул отец, приобнимая девушку на встречу.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0068 / `Борисовича`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — громко хмыкнул клановец, развалившись в кресле приемной «самого Глеба Борисовича».
- current normalized: — громко хмыкнул клановец, развалившись в кресле приемной «самого Глеба Борисовича».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0070 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки Юрий Васильевич до сих пор оставался клановцем.
- current normalized: Всё-таки Юрий Васильевич до сих пор оставался клановцем.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0077 / `во-о-от`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну во-о-от…
- current normalized: — Ну вооот…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0078 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Краем глаза он отметил, что Виктория тенью повторила его движение, а вот Мышкины подниматься на ноги что-то не спешат.
- current normalized: Краем глаза он отметил, что Виктория тенью повторила его движение, а вот Мышкины подниматься на ноги что-то не спешат.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0079 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Глеб Борисович, — довольно резко начал Волконский, примерно представлявший время реагирования тревожных групп в подобных ситуациях.
- current normalized: — Глеб Борисович, — довольно резко начал Волконский, примерно представлявший время реагирования тревожных групп в подобных ситуациях.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0083 / `Борисовичу`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: Однако Глебу Борисовичу было вовсе не до того самого кланового этикета.
- current normalized: Однако Глебу Борисовичу было вовсе не до того самого кланового этикета.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0013-p-0090 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Он еще успел заметить, как в синхронном прыжке, наплевав на все, за ним последовали Мышкины.
- current normalized: Он еще успел заметить, как в синхронном прыжке, наплевав на все, за ним последовали Мышкины.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0006 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза девушки были закрыты, щечки порозовели, а сама она, судя по легкой улыбке, чувствовала себя куда лучше, сбросив напряжение.
- current normalized: Глаза девушки были закрыты, щечки порозовели, а сама она, судя по легкой улыбке, чувствовала себя куда лучше, сбросив напряжение.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0007 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: Однако прикольные «трафареты» на покрытых ныне слоем инея стенах бойцы оставили.
- current normalized: Однако прикольные «трафареты» на покрытых ныне слоем инея стенах бойцы оставили.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0009 / `стене`
- class: стены; verdict: **OK**
- FB2 sentence: Да, его откинуло к стене.
- current normalized: Да, его откинуло к стене.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0009 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: Глеб Борисович на ногах не устоял.
- current normalized: Глеб Борисович на ногах не устоял.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0012 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Наведешь оружие на человека, а он потом с вопросами к Главе пойдет.
- current normalized: Наведешь оружие на человека, а он потом с вопросами к Главе пойдет.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0013 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Уверен, все решится в ближайшие сроки.
- current normalized: Уверен, все решится в ближайшие сроки.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0015 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза единственного пока присутствующего представителя клана, опасно блеснули.
- current normalized: Глаза единственного пока присутствующего представителя клана, опасно блеснули.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0016 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Юрий Борисович, — ровно «сорвал раздражение» он на медиамагнате.
- current normalized: — Юрий Борисович, — ровно «сорвал раздражение» он на медиамагнате.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0024 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все также внешне спокойно уточнил мужчина.
- current normalized: — все также внешне спокойно уточнил мужчина.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0026 / `Борисовича`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Грубость господина Архипова Глеба Борисовича.
- current normalized: — Грубость господина Архипова Глеба Борисовича.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0033 / `Борисовичу`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Назначил встречу Глебу Борисовичу…
- current normalized: — Назначил встречу Глебу Борисовичу…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако все присутствующие понимали, что каждое слово и движение будет позже многократно изучено группой разбора и представлено в виде расширенного доклада Главе и воеводе.
- current normalized: Однако все присутствующие понимали, что каждое слово и движение будет позже многократно изучено группой разбора и представлено в виде расширенного доклада Главе и воеводе.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0039 / `Борисовичем`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: Павел с интересом наблюдал за Глебом Борисовичем.
- current normalized: Павел с интересом наблюдал за Глебом Борисовичем.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0041 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все, кому нужно этот момент оценят и так.
- current normalized: Но все, кому нужно этот момент оценят и так.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0045 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Да, я могу закрыть глаза на неуважение.
- current normalized: Да, я могу закрыть глаза на неуважение.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0046 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: После ТАКОГО приема все это будет уже никому не интересно.
- current normalized: После ТАКОГО приема всё это будет уже никому не интересно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0050 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза обоих распахнулись от понимания, ЧТО именно один из них едва не сотворил.
- current normalized: Глаза обоих распахнулись от понимания, ЧТО именно один из них едва не сотворил.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0052 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Закрой рот, Глеб Борисович.
- current normalized: — Закрой рот, Глеб Борисович.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0055 / `Борисовичем`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Я прибыл для разговора с Глебом Борисовичем, — вновь взял слово клановец.
- current normalized: — Я прибыл для разговора с Глебом Борисовичем, — вновь взял слово клановец.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0059 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: Вот и Глеб Борисович удивленно покосился на родича.
- current normalized: Вот и Глеб Борисович удивленно покосился на родича.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0062 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Вот и прекрасно, — кивнул молодой человек, замечательно прочитав по лицу собеседника все, что ему было нужно.
- current normalized: — Вот и прекрасно, — кивнул молодой человек, замечательно прочитав по лицу собеседника все, что ему было нужно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0066 / `Борисович`
- class: Борисович; verdict: **UNRESOLVED**
- FB2 sentence: — Глеб Борисович переутомился, — отрубил представитель коменданта.
- current normalized: — Глеб Борисович переутомился, — отрубил представитель коменданта.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0067 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Местные уже сделали для него все, что могли.
- current normalized: Местные уже сделали для него все, что могли.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0014-p-0071 / `Та-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-ак…
- current normalized: — Тааак…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0006 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А начиналось все неплохо.
- current normalized: А начиналось все неплохо.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0006 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: К удивлению Сергея, его брат действительно смог согласовать тренировочный выход на один из полигонов СИБ.
- current normalized: К удивлению Сергея, его брат действительно смог согласовать тренировочный выход на один из полигонов СИБ.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Дальше все было довольно просто и привычно: сбор, размещение в глайдере, двадцать минут полета в десантном отсеке и высадка.
- current normalized: Дальше все было довольно просто и привычно: сбор, размещение в глайдере, двадцать минут полета в десантном отсеке и высадка.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0010 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: — Ну, привет, волчата, — хмыкнула она с высоты опыта заслуженного волкодава.
- current normalized: — Ну, привет, волчата, — хмыкнула она с высоты опыта заслуженного волкодава.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0013 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Обычно хоть какая-то информация по объекту все-таки была.
- current normalized: Обычно хоть какая-то информация по объекту всё-таки была.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0019 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Именно в этот момент кое-кому в голову стали закрадываться первые мысли о том, что, возможно, все может оказаться не так просто, как могло бы показаться.
- current normalized: Именно в этот момент кое-кому в голову стали закрадываться первые мысли о том, что, возможно, все может оказаться не так просто, как могло бы показаться.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0027 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но руку в универсальном жесте, мол, все готово, он поднял.
- current normalized: Но руку в универсальном жесте, мол, все готово, он поднял.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0028 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — тут же рявкнула действующая сотрудница СИБ.
- current normalized: — тут же рявкнула действующая сотрудница СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0031 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки досталось всем очень неплохо.
- current normalized: Всё-таки досталось всем очень неплохо.
- current rule: `lexicon.project, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0034 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все это было каких-то шестнадцать часов назад.
- current normalized: Всё это было каких-то шестнадцать часов назад.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0046 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все равно темно и ничего не видно.
- current normalized: Всё равно темно и ничего не видно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0064 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — Значит, время играет против нас, — подытожил Костя, краем глаза отметив как быстро светлеет небо.
- current normalized: — Значит, время играет против нас, — подытожил Костя, краем глаза отметив как быстро светлеет небо.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0065 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А это значит, что курсанты с каждым часом теряют силы в то время как их противник остается все столь же бодр.
- current normalized: А это значит, что курсанты с каждым часом теряют силы в то время как их противник остается все столь же бодр.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0071 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Три фигуры бесшумными тенями бросились на беззаботно вышагивающую по тропинке девушку со светящимися Льдом глазами.
- current normalized: Три фигуры бесшумными тенями бросились на беззаботно вышагивающую по тропинке девушку со светящимися Льдом глазами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0072 / `ВЖУ-У-УХ`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: ВЖУ-У-УХ!
- current normalized: ВЖУУУХ!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0073 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако досталось все же куда меньше, чем остальным.
- current normalized: Однако досталось всё же куда меньше, чем остальным.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0073 / `Стена`
- class: стены; verdict: **OK**
- FB2 sentence: Стена ледяного ветра откинула в сторону парней.
- current normalized: Стена ледяного ветра откинула в сторону парней.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0015-p-0091 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: Однако этого краткого мига вполне хватило Павлу, чтобы отметить один важный нюанс: в глазах «принцесски» не осталось и следа вчерашнего безумия и раздражения.
- current normalized: Однако этого краткого мига вполне хватило Павлу, чтобы отметить один важный нюанс: в глазах «принцесски» не осталось и следа вчерашнего безумия и раздражения.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0007 / `Фу-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Фу-у-у-ф…
- current normalized: — Фууу-ф…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0013 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: А это помещение защищено от чужих глаз и ушей получше иного центра управления Волконских.
- current normalized: А это помещение защищено от чужих глаз и ушей получше иного центра управления Волконских.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0022 / `Прекра-а-а-асно`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Прекра-а-а-асно, — протянул Глава, с великим тщанием устанавливая очередной «кирпичик» на законное место.
- current normalized: — Прекрааасно, — протянул Глава, с великим тщанием устанавливая очередной «кирпичик» на законное место.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0027 / `Фу-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Фу-у-у-у…
- current normalized: — Фууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0045 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ради такого дела собраться должны были все.
- current normalized: Ради такого дела собраться должны были все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0050 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Впрочем, не слишком удивительной, на фоне работы в городе боевого глайдера, но все же…
- current normalized: Впрочем, не слишком удивительной, на фоне работы в городе боевого глайдера, но всё же…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0055 / `Та-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-ак!
- current normalized: — Тааак!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0064 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все это, конечно…
- current normalized: — Всё это, конечно…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0067 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А еще через миг позволил себе глупую ухмылку (все равно никто никогда не увидит!
- current normalized: А еще через миг позволил себе глупую ухмылку (всё равно никто никогда не увидит!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0078 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако в данном случае все было несколько сложнее.
- current normalized: Однако в данном случае все было несколько сложнее.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0102 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Шутка бородатая, но все-таки.
- current normalized: Шутка бородатая, но всё-таки.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0114 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Ну, раз с этим вопросом решили, — бодро сообщил Волконский, неосознанно подкинув гранату на ладони (все равно без вкрученного запала ее подорвать будет довольно сложно, а они, родимые, сейчас вовсе не на штатном месте, а рядком на той же кровати лежат.
- current normalized: — Ну, раз с этим вопросом решили, — бодро сообщил Волконский, неосознанно подкинув гранату на ладони (всё равно без вкрученного запала ее подорвать будет довольно сложно, а они, родимые, сейчас вовсе не на штатном месте, а рядком на той же кровати лежат.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0116 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Юсупова, все еще провожающая взглядом каждый взлет ребристого корпуса, чуть заторможенно кивнула.
- current normalized: Юсупова, всё еще провожающая взглядом каждый взлет ребристого корпуса, чуть заторможенно кивнула.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0126 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — С тобой все в порядке?
- current normalized: — С тобой все в порядке?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0127 / `Потом`
- class: потом; verdict: **OK**
- FB2 sentence: Потом — по выбору.
- current normalized: Потом — по выбору.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0016-p-0132 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Оставалось лишь надеяться, что Светланка, прекрасно понимающая, куда и зачем они все вместе направляются, поторопит «уралочку».
- current normalized: Оставалось лишь надеяться, что Светланка, прекрасно понимающая, куда и зачем они все вместе направляются, поторопит «уралочку».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0003 / `во-о-о-о-он`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Нет, зная Павла, можно, конечно, предположить, что во-о-о-о-он тот ржавый чуть ли не до сквозных дыр микроавтобус или откровенно ушатаный седан, возле которого постоянно крутилась компашка довольно маргинального вида (девушка частенько наблюдала за ними в окно) дожидается именно их.
- current normalized: Нет, зная Павла, можно, конечно, предположить, что вооон тот ржавый чуть ли не до сквозных дыр микроавтобус или откровенно ушатаный седан, возле которого постоянно крутилась компашка довольно маргинального вида (девушка частенько наблюдала за ними в окно) дожидается именно их.
- current rule: `lexicon.project, prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0012 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Они все-таки прособирались.
- current normalized: Они всё-таки прособирались.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0012 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А потому все остальные действующие лица уже собрались.
- current normalized: А потому все остальные действующие лица уже собрались.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0012 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: А потому все остальные действующие лица уже собрались.
- current normalized: А потому все остальные действующие лица уже собрались.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Судя по тому, как вытянулось личико девушки, потрясений ей достанется все-таки три.
- current normalized: Судя по тому, как вытянулось личико девушки, потрясений ей достанется всё-таки три.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0016 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки из окна авто или родовой высотки было достаточно сложно оценить размах дворов.
- current normalized: Всё-таки из окна авто или родовой высотки было достаточно сложно оценить размах дворов.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0016 / `высотки`
- class: высоты; verdict: **OK**
- FB2 sentence: Все-таки из окна авто или родовой высотки было достаточно сложно оценить размах дворов.
- current normalized: Всё-таки из окна авто или родовой высотки было достаточно сложно оценить размах дворов.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0018 / `высотке`
- class: высоты; verdict: **OK**
- FB2 sentence: Конечно, клановцы, тем более, если речь шла о Юсуповых, могли позволить себе просторные покои даже в высотке.
- current normalized: Конечно, клановцы, тем более, если речь шла о Юсуповых, могли позволить себе просторные покои даже в высотке.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0019 / `высотки`
- class: высоты; verdict: **OK**
- FB2 sentence: А зачем, если есть глайдер, который доставит из высотки, где ты живешь…
- current normalized: А зачем, если есть глайдер, который доставит из высотки, где ты живешь…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0019 / `высотку`
- class: высоты; verdict: **OK**
- FB2 sentence: в другую высотку, где расположены магазины, клубы, рестораны или иные «блага»?
- current normalized: в другую высотку, где расположены магазины, клубы, рестораны или иные «блага»?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0024 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Вот только представляла все это она немного по-другому.
- current normalized: Вот только представляла всё это она немного по-другому.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0031 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Волконский не стал уточнять, что все эти пункты давно закрыты родичами «уралочки» в рамках тех самых «счетов за неудобства».
- current normalized: Волконский не стал уточнять, что все эти пункты давно закрыты родичами «уралочки» в рамках тех самых «счетов за неудобства».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако все они спешили по своим делам, никакого внимания не обращая компанию из парня и пары девушек.
- current normalized: Однако все они спешили по своим делам, никакого внимания не обращая компанию из парня и пары девушек.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0054 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — О, не волнуйся, скоро все будет очень хорошо!..
- current normalized: — О, не волнуйся, скоро все будет очень хорошо!..
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0058 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: Больше всего Главе одного из старейших кланов империи хотелось швырнуть ни в чем не повинный гаджет в стену.
- current normalized: Больше всего Главе одного из старейших кланов империи хотелось швырнуть ни в чем не повинный гаджет в стену.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0065 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но как же оно все не ко времени!
- current normalized: Но как же оно все не ко времени!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0070 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Однако сначала служба безопасности Волконских не сочла его серьезной фигурой, а потом было поздно — за каких-то пятнадцать лет бывший заместитель по операционной деятельности старшего казначея этот самый совет возглавил.
- current normalized: Однако сначала служба безопасности Волконских не сочла его серьезной фигурой, а пот+ом было поздно — за каких-то пятнадцать лет бывший заместитель по операционной деятельности старшего казначея этот самый совет возглавил.
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0081 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Толя, я все понимаю, но мне необходима встреча с Павлом.
- current normalized: — Толя, я все понимаю, но мне необходима встреча с Павлом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0017-p-0083 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: — У моего сына свои требования по части безопасности, — сообщил со странным выражением лица зам.
- current normalized: — У моего сына свои требования по части безопасности, — сообщил со странным выражением лица зам.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0021 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — И, напомню, ты заранее согласился на все условия Павла.
- current normalized: — И, напомню, ты заранее согласился на все условия Павла.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0025 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мол, решился, или стоит все отменить и согласовать новую встречу?
- current normalized: Мол, решился, или стоит все отменить и согласовать новую встречу?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0027 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: В глазах собеседника на короткий миг вспыхнуло странное торжество.
- current normalized: В глазах собеседника на короткий миг вспыхнуло странное торжество.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0029 / `ВСЕ`
- class: все/всё; verdict: **OK**
- FB2 sentence: Согласился на ВСЕ условия — терпи.
- current normalized: Согласился на ВСЕ условия — терпи.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0032 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: На этом полномочия «личников» — все.
- current normalized: На этом полномочия «личников» — все.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0034 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все остальное — забота…
- current normalized: — Всё остальное — забота…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0045 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Едут, — коротко сообщил начальник «лички», которому все не нравилось еще больше, чем его господину.
- current normalized: — Едут, — коротко сообщил начальник «лички», которому все не нравилось еще больше, чем его господину.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0052 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Та, правда, все равно ничего не скрывала.
- current normalized: Та, правда, всё равно ничего не скрывала.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0052 / `стрелка`
- class: стрелку; verdict: **OK**
- FB2 sentence: Первыми на гладкий бетон паркинга ступили покинувший салон Павел и ехавшая «за стрелка» Катерина.
- current normalized: Первыми на гладкий бетон паркинга ступили покинувший салон Павел и ехавшая «за стрелка» Катерина.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0053 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все четверо были одеты…
- current normalized: Все четверо были одеты…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0056 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — Безопасность в пути и во время пребывания на объекте будет обеспечена сводной группой СИБ…
- current normalized: — Безопасность в пути и во время пребывания на объекте будет обеспечена сводной группой СИБ…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0072 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Коллеги фиолетововолосой моментально засекретили все, до чего смогли дотянуться.
- current normalized: Коллеги фиолетововолосой моментально засекретили все, до чего смогли дотянуться.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0075 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — И все же!..
- current normalized: — И всё же!..
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0087 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все трое Волконских как-то разом напряглись.
- current normalized: Все трое Волконских как-то разом напряглись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0103 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Где еще потом такого специалиста сыскать.
- current normalized: Где еще потом такого специалиста сыскать.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0104 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — Угу, — задумчиво кивнул молодой человек и на миг прикрыл глаза.
- current normalized: — Угу, — задумчиво кивнул молодой человек и на миг прикрыл глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0105 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все трое «гостей», не сговариваясь, обернулись.
- current normalized: Все трое «гостей», не сговариваясь, обернулись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0106 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все произошло обыденно и быстро.
- current normalized: Все произошло обыденно и быстро.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0107 / `хлопок`
- class: хлопок; verdict: **OK**
- FB2 sentence: Глухой хлопок удара тут же донесся до пассажиров микроавтобуса.
- current normalized: Глухой хлопок удара тут же донесся до пассажиров микроавтобуса.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0117 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Тем более ситуация казалась обидней, что он добровольно и заранее на все согласился.
- current normalized: Тем более ситуация казалась обидней, что он добровольно и заранее на все согласился.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0138 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: — чуть запнулась Светлана Волконская, краем глаза заметив наблюдателей.
- current normalized: — чуть запнулась Светлана Волконская, краем глаза заметив наблюдателей.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0138 / `Ви-и-и-и`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Держи, Ви-и-и-и…
- current normalized: — Держи, Виии…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0143 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Резко обернувшись, она также застыла на миг, после чего ее глаза натурально полыхнули Льдом.
- current normalized: Резко обернувшись, она также застыла на миг, после чего ее глаза натурально полыхнули Льдом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0148 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все будет готово через пять минут, — сообщила «принцесса» не оборачиваясь.
- current normalized: — Все будет готово через пять минут, — сообщила «принцесса» не оборачиваясь.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0018-p-0150 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки переговоры начались очень уж странно!
- current normalized: Всё-таки переговоры начались очень уж странно!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0013 / `стенд`
- class: стены; verdict: **OK**
- FB2 sentence: А вот справа был установлен стенд под легкие бронедоспехи.
- current normalized: А вот справа был установлен стенд под легкие бронедоспехи.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0015 / `стрелковки`
- class: стрелку; verdict: **OK**
- FB2 sentence: И не столько среди стрелковки, сколько на стеллажах с инженеркой.
- current normalized: И не столько среди стрелковки, сколько на стеллажах с инженеркой.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0017 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: После сытного обеда, гостей вновь усадили все в тот же микроавтобус.
- current normalized: После сытного обеда, гостей вновь усадили все в тот же микроавтобус.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0029 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: чтобы потом использовать нынешний отказ на совершенно другом поле боя.
- current normalized: чтобы потом использовать нынешний отказ на совершенно другом поле боя.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0037 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Он прекрасно помнил, в каком предвкушении блеснули глаза племянника, стоило упомянуть, что Совет занимается распределением вполне себе приличных бюджетов, в том числе и на культурно-просветительские цели.
- current normalized: Он прекрасно помнил, в каком предвкушении блеснули глаза племянника, стоило упомянуть, что Совет занимается распределением вполне себе приличных бюджетов, в том числе и на культурно-просветительские цели.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0040 / `высоты`
- class: высоты; verdict: **OK**
- FB2 sentence: Картина с высоты была…
- current normalized: Картина с высоты была…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0041 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все-таки интересно, кто именно за этим стоит?
- current normalized: — Всё-таки интересно, кто именно за этим стоит?
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0050 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мужчина исчерпал уже все время, что выделил на сегодня для решения вопроса «Павел Анатольевич Волконский».
- current normalized: Мужчина исчерпал уже всё время, что выделил на сегодня для решения вопроса «Павел Анатольевич Волконский».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0059 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Возможно, сообщив вам о том, что ожидаю важных гостей, все-таки стоило уточнить кого именно.
- current normalized: — Возможно, сообщив вам о том, что ожидаю важных гостей, всё-таки стоило уточнить кого именно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0061 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А вот он все же погодил.
- current normalized: А вот он всё же погодил.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0067 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: — хищно улыбнулась сестренка, блеснув глазками.
- current normalized: — хищно улыбнулась сестренка, блеснув глазками.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0070 / `глазки`
- class: глаза; verdict: **OK**
- FB2 sentence: Его сузившие глазки-пуговки не предвещали помощнику ничего хорошего.
- current normalized: Его сузившие глазки-пуговки не предвещали помощнику ничего хорошего.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0079 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Так, все на этого Павла!
- current normalized: — Так, все на этого Павла!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0082 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: все⁈
- current normalized: все?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0092 / `высоте`
- class: высоты; verdict: **OK**
- FB2 sentence: — Глайдеров, говоришь, — призадумался Гавр Петрович, припоминая, как совсем недавно весь клан стоял на ушах из-за боевой машины, «гарцующей» в центре столицы на сверхмалой высоте.
- current normalized: — Глайдеров, говоришь, — призадумался Гавр Петрович, припоминая, как совсем недавно весь клан стоял на ушах из-за боевой машины, «гарцующей» в центре столицы на сверхмалой высоте.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0019-p-0094 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Лавры лаврами, но деньги все-таки лучше.
- current normalized: Лавры лаврами, но деньги всё-таки лучше.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0010 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все также продолжил изучать внутренний мир наколотых на вилку представителей семейства бобовых.
- current normalized: Все также продолжил изучать внутренний мир наколотых на вилку представителей семейства бобовых.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0023 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все было неправильно!
- current normalized: Все было неправильно!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0037 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки беседа беседой, но необходимость подкрепиться перед следующим учебным блоком никто не отменял.
- current normalized: Всё-таки беседа беседой, но необходимость подкрепиться перед следующим учебным блоком никто не отменял.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0041 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза Андрей удивленно расширились.
- current normalized: Глаза Андрей удивленно расширились.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0045 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза «гостя» распахнулись еще шире.
- current normalized: Глаза «гостя» распахнулись еще шире.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0045 / `родов`
- class: родов; verdict: **OK**
- FB2 sentence: Обычно к реестру кланов и родов империи обращаются лишь для проверки конкретных персоналий перед операцией, либо во время планирования интриг.
- current normalized: Обычно к реестру кланов и родов империи обращаются лишь для проверки конкретных персоналий перед операцией, либо во время планирования интриг.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0048 / `Э-э-эй`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Э-э-эй!
- current normalized: — ЭЭЭй!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0057 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все были заняты штурмом центрального выхода, и каждого куда больше волновал вопрос, как не быть задавленным, чем события на другом конце Главного зала.
- current normalized: Вс+е были заняты штурмом центрального выхода, и каждого куда больше волновал вопрос, как не быть задавленным, чем события на другом конце Главного зала.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0062 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И, возможно, ему было бы даже стыдно, если все произошедшее не было последствиями плана СИБ, а вовсе не его собственного.
- current normalized: И, возможно, ему было бы даже стыдно, если все произошедшее не было последствиями плана СИБ, а вовсе не его собственного.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0062 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: И, возможно, ему было бы даже стыдно, если все произошедшее не было последствиями плана СИБ, а вовсе не его собственного.
- current normalized: И, возможно, ему было бы даже стыдно, если все произошедшее не было последствиями плана СИБ, а вовсе не его собственного.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0064 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В этот миг Андрей имел вид человека, который мысленно плюнул на все, а потому он раздраженно махнул рукой и выпалил:
- current normalized: В этот миг Андрей имел вид человека, который мысленно плюнул на все, а потому он раздраженно махнул рукой и выпалил:
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0067 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: ко всему этому, — чуть тише, но все с той же твердостью во взоре закончил Архипов.
- current normalized: ко всему этому, — чуть тише, но все с той же твердостью во взоре закончил Архипов.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0068 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Тот все также спокойно прожевал очередной кусочек запеченной под сырной корочкой говядины и, лишь неспешно с ним «расправившись», уточнил:
- current normalized: Тот все также спокойно прожевал очередной кусочек запеченной под сырной корочкой говядины и, лишь неспешно с ним «расправившись», уточнил:
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0083 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: — Отправь его представителю СИБ.
- current normalized: — Отправь его представителю СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0087 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Краем глаза он отметил чуть напрягшихся девушек.
- current normalized: Краем глаза он отметил чуть напрягшихся девушек.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0094 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: На целого нового представителя СИБ при Классах.
- current normalized: На целого нового представителя СИБ при Классах.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0100 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все также спокойно поинтересовался Волконский, единственный из присутствующих знавший, что собеседница была в составе нападавших.
- current normalized: — все также спокойно поинтересовался Волконский, единственный из присутствующих знавший, что собеседница была в составе нападавших.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0100 / `нападавших`
- class: нападавших; verdict: **OK**
- FB2 sentence: — все также спокойно поинтересовался Волконский, единственный из присутствующих знавший, что собеседница была в составе нападавших.
- current normalized: — все также спокойно поинтересовался Волконский, единственный из присутствующих знавший, что собеседница была в составе нападавших.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0109 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: В конце концов, если уж СИБ не имеет претензий к бывшему сопернику, то и у него вопросов быть не должно.
- current normalized: В конце концов, если уж СИБ не имеет претензий к бывшему сопернику, то и у него вопросов быть не должно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0020-p-0134 / `стрелкового`
- class: стрелку; verdict: **OK**
- FB2 sentence: В этот раз в него уперся не только холодный взгляд, но и ствол стрелкового комплекса.
- current normalized: В этот раз в него уперся не только холодный взгляд, но и ствол стрелкового комплекса.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0005 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Слово «откупиться» в данном контексте звучало грубовато, а потому все предпочитали куда более обтекаемый термин.
- current normalized: Слово «откупиться» в данном контексте звучало грубовато, а потому вс+е предпочитали куда более обтекаемый термин.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0008 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Всем и так все было понятно.
- current normalized: Всем и так все было понятно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0011 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И пусть самой Светлане было все равно, но она довольно умело била по болевым точкам.
- current normalized: И пусть самой Светлане было всё равно, но она довольно умело била по болевым точкам.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0016 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ничего, все впереди.
- current normalized: Ничего, все впереди.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0023 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: — Не сомневаюсь, — хмыкнула Светлана, лукаво блеснув глазками.
- current normalized: — Не сомневаюсь, — хмыкнула Светлана, лукаво блеснув глазками.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0035 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Предпочитают дать добровольное согласие на проведение аудита и решить все вопросы в частном порядке.
- current normalized: Предпочитают дать добровольное согласие на проведение аудита и решить все вопросы в частном порядке.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0047 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все что угодно, лишь бы задобрить «строгого, но справедливого» проверяющего.
- current normalized: Все что угодно, лишь бы задобрить «строгого, но справедливого» проверяющего.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0050 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все-таки умудрилась не подавиться душистым ароматным напитком.
- current normalized: Но всё-таки умудрилась не подавиться душистым ароматным напитком.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0072 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Гавр Петрович зло сощурил глаза, после чего прошипел.
- current normalized: Гавр Петрович зло сощурил глаза, после чего прошипел.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0073 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И где они все!
- current normalized: И где они все!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0021-p-0074 / `стрелка`
- class: стрелку; verdict: **OK**
- FB2 sentence: Теперь ее взгляд куда больше напоминал холодный взор стрелка.
- current normalized: Теперь ее взгляд куда больше напоминал холодный взор стрелка.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0003 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И лет вот уж пятнадцать как имел особую надбавку к жалованию за то, что всегда помнил одну-единственную истину: «Все Волконские равны, но иные все же равнее!
- current normalized: И лет вот уж пятнадцать как имел особую надбавку к жалованию за то, что всегда помнил одну-единственную истину: «Все Волконские равны, но иные всё же равнее!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И лет вот уж пятнадцать как имел особую надбавку к жалованию за то, что всегда помнил одну-единственную истину: «Все Волконские равны, но иные все же равнее!
- current normalized: И лет вот уж пятнадцать как имел особую надбавку к жалованию за то, что всегда помнил одну-единственную истину: «Все Волконские равны, но иные всё же равнее!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0005 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В конце концов, платить соглашались все.
- current normalized: В конце концов, платить соглашались все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0017 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В целом, ему было все равно.
- current normalized: В целом, ему было всё равно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0019 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Что-то ему сегодня все это не нравилось.
- current normalized: Что-то ему сегодня всё это не нравилось.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0032 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все еще удивленно, но ничуть не обеспокоенно, вскинул брови молодой человек.
- current normalized: — всё еще удивленно, но ничуть не обеспокоенно, вскинул брови молодой человек.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0048 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все будет.
- current normalized: — Все будет.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0079 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: » — жестом отдал он команду, едва убедился, что все три группы грамотно втянулись на территорию.
- current normalized: » — жестом отдал он команду, едва убедился, что все три группы грамотно втянулись на территорию.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0080 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: — прозвучала негромкая, но доходчивая команда откуда-то сверху, а у глаз вдруг возникло матовое лезвие боевого десантного тесака.
- current normalized: — прозвучала негромкая, но доходчивая команда откуда-то сверху, а у глаз вдруг возникло матовое лезвие боевого десантного тесака.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0087 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все замерли, глядя куда-то за спину командиру.
- current normalized: Вс+е замерли, глядя куда-то за спину командиру.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0094 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: и тонкому таланту подмахнуть любую бумажку, ничуть не заботясь о том, что когда-нибудь все-таки наступит «завтра».
- current normalized: и тонкому таланту подмахнуть любую бумажку, ничуть не заботясь о том, что когда-нибудь всё-таки наступит «завтра».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0097 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Они хоть и привычные уже были, но все ж бесплатный цирк до сих пор не надоел.
- current normalized: Они хоть и привычные уже были, но всё ж бесплатный цирк до сих пор не надоел.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0111 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: нарушение все равно будут найдены.
- current normalized: нарушение всё равно будут найдены.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0112 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все эти мысли пронеслись в одно мгновение, но тут же отправились на задворки сознания, изгнанные простым пониманием: за воротами действительно не было никого.
- current normalized: Все эти мысли пронеслись в одно мгновение, но тут же отправились на задворки сознания, изгнанные простым пониманием: за воротами действительно не было никого.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0114 / `здра-а-а-асти`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну, здра-а-а-асти!
- current normalized: — Ну, здрааасти!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0022-p-0115 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Краем глаза Крючков успел заметить тень тяжелого меха, вставшего на места выбитых ворот.
- current normalized: Краем глаза Крючков успел заметить тень тяжелого меха, вставшего на места выбитых ворот.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0004 / `здра-а-а-асти`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Просто попытался помочь определиться с ответом на его протяжное «здра-а-а-асти»…
- current normalized: Просто попытался помочь определиться с ответом на его протяжное «здрааасти»…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0012 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: все?
- current normalized: все?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0019 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все-таки собрался с душевными ресурсами организатор комиссии.
- current normalized: — всё-таки собрался с душевными ресурсами организатор комиссии.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0020 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Но все-таки «боевой отметиной» обзавелся.
- current normalized: Но всё-таки «боевой отметиной» обзавелся.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0020 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Да, целители все сведут моментально.
- current normalized: Да, целители вс+е сведут моментально.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0027 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Имя Гавра Петровича все прекрасно знали.
- current normalized: Имя Гавра Петровича все прекрасно знали.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0028 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — У меня приказ, — все же попытался привести аргумент помощник «патриарха».
- current normalized: — У меня приказ, — всё же попытался привести аргумент помощник «патриарха».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0048 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все как-то не в самом неприятном смысле.
- current normalized: И все как-то не в самом неприятном смысле.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0051 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Павел, — гордо вскинул все свои подбородки он и усмехнулся победно.
- current normalized: — Павел, — гордо вскинул все свои подбородки он и усмехнулся победно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0054 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза «творца» горели праведным гневом и уверенностью в своей правоте.
- current normalized: Глаза «творца» горели праведным гневом и уверенностью в своей правоте.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0056 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: «Великий художник», похоже, исчерпал и без того невеликий запас «смелости» в короткой истерике, а потому притих, глядя на окружающих грустными глазками какающего котика.
- current normalized: «Великий художник», похоже, исчерпал и без того невеликий запас «смелости» в короткой истерике, а потому притих, глядя на окружающих грустными глазками какающего котика.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0060 / `стенды`
- class: стены; verdict: **OK**
- FB2 sentence: Однако отчего-то ответственного за организацию всего этого безобразия абсолютно не заинтересовал глайдер и тестовые стенды.
- current normalized: Однако отчего-то ответственного за организацию всего этого безобразия абсолютно не заинтересовал глайдер и тестовые стенды.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0062 / `стрелковыми`
- class: стрелку; verdict: **OK**
- FB2 sentence: — Дышат, — заверил Павел, кивнув нескольким бойцам с автоматическими стрелковыми комплексами в руках.
- current normalized: — Дышат, — заверил Павел, кивнув нескольким бойцам с автоматическими стрелковыми комплексами в руках.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0064 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все просто.
- current normalized: — Все просто.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0095 / `глазоньки`
- class: глаза; verdict: **OK**
- FB2 sentence: Однако прежде чем закатить глазоньки в возможно даже непритворном обмороке, он успел подергать за руку седого мужчину лет пятидесяти на вид.
- current normalized: Однако прежде чем закатить глазоньки в возможно даже непритворном обмороке, он успел подергать за руку седого мужчину лет пятидесяти на вид.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0099 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Краем глаза наблюдая за метаниями Гавра Петровича по ее кабинету.
- current normalized: Краем глаза наблюдая за метаниями Гавра Петровича по ее кабинету.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0101 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Самая натуральная потеря лица выходит…
- current normalized: Самая натуральная потеря лица выходит…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0102 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Ты будешь платить как все!
- current normalized: — Ты будешь платить как все!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0115 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако и без слов все стало как-то очень даже ясно.
- current normalized: Однако и без слов все стало как-то очень даже ясно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0119 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: С эмблемами СИБ.
- current normalized: С эмблемами СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0120 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И тот факт (о котором мужчина все равно не узнал), что «сторож» отделался лишь шишкой на лбу, с формальной точки зрения ничего не менял.
- current normalized: И тот факт (о котором мужчина всё равно не узнал), что «сторож» отделался лишь шишкой на лбу, с формальной точки зрения ничего не менял.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0121 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Я все расскажу, — глухо выдавил из себя теперь уже действительно похожий на старика глава Совета.
- current normalized: — Я все расскажу, — глухо выдавил из себя теперь уже действительно похожий на старика глава Совета.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0127 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — пусть и напряженно, но все же довольно ровно поинтересовалась невысокая непримечательная женщина лет шестидесяти, сосредоточив на Главе свой невыразительный взгляд.
- current normalized: — пусть и напряженно, но всё же довольно ровно поинтересовалась невысокая непримечательная женщина лет шестидесяти, сосредоточив на Главе свой невыразительный взгляд.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0135 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: — Забыли, на чей именно объект положили глаз?
- current normalized: — Забыли, на чей именно объект положили глаз?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0142 / `Ни-и-и-ика`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ни-и-и-ика Андреевна-а-а-а…
- current normalized: — Нииика Андреевнааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0142 / `Андреевна-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ни-и-и-ика Андреевна-а-а-а…
- current normalized: — Нииика Андреевнааа…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0142 / `Семео-о-он`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — протянул Глава с интонациями героя очень древнего фильма: «Семео-о-он Семео-о-о-оныч!
- current normalized: — протянул Глава с интонациями героя очень древнего фильма: «Семеооон Семеоооныч!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0142 / `Семео-о-о-оныч`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — протянул Глава с интонациями героя очень древнего фильма: «Семео-о-он Семео-о-о-оныч!
- current normalized: — протянул Глава с интонациями героя очень древнего фильма: «Семеооон Семеоооныч!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0145 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Все ясно!
- current normalized: «Все ясно!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0145 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Да, большую часть «налогов» придется отменить, но не все, не все…
- current normalized: Да, большую часть «налогов» придется отменить, но не все, не все…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0023-p-0145 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Да, большую часть «налогов» придется отменить, но не все, не все…
- current normalized: Да, большую часть «налогов» придется отменить, но не все, не все…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0003 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Застыли все.
- current normalized: Застыли все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0007 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все словно ожили и вернулись к прерванным занятиям.
- current normalized: Все словно ожили и вернулись к прерванным занятиям.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0007 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И, что характерно, все на Волконского.
- current normalized: И, что характерно, все на Волконского.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0010 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Словно дерзкая и уверенная в себе по самые помидоры еще минуту назад троица всерьез опасалась, что стоит кому-то отвести глаза, и их противница бросится в самоубийственную атаку словно раненая тигрица, защищающая своих котят.
- current normalized: Словно дерзкая и уверенная в себе по самые помидоры еще минуту назад троица всерьез опасалась, что стоит кому-то отвести глаза, и их противница бросится в самоубийственную атаку словно раненая тигрица, защищающая своих котят.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0015 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Та все также застыла статуей в малом поклоне, сложив руки перед собой на манер горничных из вновь набирающих популярность корейских дорам (на этом моменте Павел клятвенно пообещал себе вставить втык Бешеной, чтобы думала чему «небожительниц» учит!
- current normalized: Та все также застыла статуей в малом поклоне, сложив руки перед собой на манер горничных из вновь набирающих популярность корейских дорам (на этом моменте Павел клятвенно пообещал себе вставить втык Бешеной, чтобы думала чему «небожительниц» учит!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0017 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все началось три дня назад.
- current normalized: Все началось три дня назад.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0017 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: А потому Волконский договаривался насчет полигонов, чтобы не пичкать девушку специально разработанными для таких случаев седативными средствами и запирать ее в четырех стенах, заблокировав комнату «оградником».
- current normalized: А потому Волконский договаривался насчет полигонов, чтобы не пичкать девушку специально разработанными для таких случаев седативными средствами и запирать ее в четырех стенах, заблокировав комнату «оградником».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0021 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Однако ей все еще было непросто.
- current normalized: Однако ей всё еще было непросто.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0021 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Правда, все больше морально.
- current normalized: Правда, всё больше морально.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0027 / `Фшу-у-у-ух`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Фшу-у-у-ух!
- current normalized: Фшууух!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0028 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: От неожиданности он выпучил глаза и буквально прыснул так и не проглоченным глотком.
- current normalized: От неожиданности он выпучил глаза и буквально прыснул так и не проглоченным глотком.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0029 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: — Пробую себя в новом качестве, — невозмутимо сообщила Виктория, отбрасывая «слипшиеся» волосы с мокрого лица.
- current normalized: — Пробую себя в новом качестве, — невозмутимо сообщила Виктория, отбрасывая «слипшиеся» волосы с мокрого лица.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0031 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Ее глаза в удивлении распахнулись, а рука сама потянулась к влажному лицу «принцессы».
- current normalized: Ее глаза в удивлении распахнулись, а рука сама потянулась к влажному лицу «принцессы».
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0035 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Все в порядке, Паша.
- current normalized: «Все в порядке, П+аша.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ведь благодаря чертовому расписанию, он попросту не имел возможности беззаботно помахать «уралочке» рукой со словами «Ну, все, удачи!
- current normalized: Ведь благодаря чертовому расписанию, он попросту не имел возможности беззаботно помахать «уралочке» рукой со словами «Ну, все, удачи!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Не-е-ет, на этой неделе почти все занятия у них были совместными.
- current normalized: Нееет, на этой неделе почти все занятия у них были совместными.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А ведь за все возможные зверства и разрушения рук «принцессы», как Главе Рода, отвечать придется именно ему.
- current normalized: А ведь за все возможные зверства и разрушения рук «принцессы», как Главе Рода, отвечать придется именно ему.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0038 / `Не-е-ет`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: Не-е-ет, на этой неделе почти все занятия у них были совместными.
- current normalized: Нееет, на этой неделе почти все занятия у них были совместными.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0039 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Естественно, все это было обставлено с соблюдением всех существующих правил приличия, а тон к делу не пришьешь.
- current normalized: Естественно, всё это было обставлено с соблюдением всех существующих правил приличия, а тон к делу не пришьешь.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0040 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Он до сих пор помнил, как замер тогда, обливаясь потом.
- current normalized: Он до сих пор помнил, как замер тогда, обливаясь потом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0045 / `Глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Глаза Виктории же, напротив, удивленно распахнулись.
- current normalized: Глаза Виктории же, напротив, удивленно распахнулись.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0047 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: С их точки зрения, все выглядело логично.
- current normalized: С их точки зрения, все выглядело логично.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0050 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Все как всегда!
- current normalized: «Все как всегда!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0051 / `Фу-у-у-у-у-ух`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Фу-у-у-у-у-ух-х-х…
- current normalized: — Фууух-х-х…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0054 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: — переспросила Виктория, припомнив недавний разговор с Кошкиной, которая пыталась ее переубедить отправиться бить лица расшумевшейся под их окнами компании.
- current normalized: — переспросила Виктория, припомнив недавний разговор с Кошкиной, которая пыталась ее переубедить отправиться бить лица расшумевшейся под их окнами компании.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0058 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Далеко не все оказались готовы к «сногсшибательной» волне чистой Силы.
- current normalized: Далеко не вс+е оказались готовы к «сногсшибательной» волне чистой Силы.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0066 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Единственное, что примиряло с ситуацией известного в империи и за ее пределами исследователя международного права — более чем щедрая оплата его услуг, с лихвой перекрывающая все риски.
- current normalized: Единственное, что примиряло с ситуацией известного в империи и за ее пределами исследователя международного права — более чем щедрая оплата его услуг, с лихвой перекрывающая все риски.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0066 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А все это требовало огромных даже по меркам его более чем нескромного дохода сумм.
- current normalized: А всё это требовало огромных даже по меркам его более чем нескромного дохода сумм.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0071 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: От одного тона девушки все надежды молодого человека на спокойный почти семейный обед в компании Вики и Светы разом рухнули.
- current normalized: От одного тона девушки все надежды молодого человека на спокойный почти семейный обед в компании Вики и Светы разом рухнули.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0075 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки целительница практически в любой семье была бы желанным пополнением.
- current normalized: Всё-таки целительница практически в любой семье была бы желанным пополнением.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0077 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Кошкины все равно оказывались на грани разорения.
- current normalized: Кошкины всё равно оказывались на грани разорения.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0077 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Во всех иных случаях они отдадут все.
- current normalized: Во всех иных случаях они отдадут все.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0083 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Красивые глаза Елены заметно погрустнели.
- current normalized: Красивые глаза Елены заметно погрустнели.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0091 / `глаз`
- class: глаза; verdict: **OK**
- FB2 sentence: Одним точным и ловким движением он наколол кочанчик брокколи на зубчики и поднял «добычу» на уровень глаз, после чего задумчиво уставился половинку соцветия.
- current normalized: Одним точным и ловким движением он наколол кочанчик брокколи на зубчики и поднял «добычу» на уровень глаз, после чего задумчиво уставился половинку соцветия.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0093 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Родился с серебряной ложкой в заднице и считаешь, что все можно, да⁈
- current normalized: Родился с серебряной ложкой в заднице и считаешь, что все можно, да?!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0097 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: На его памяти там все было немножечко не так.
- current normalized: На его памяти там все было немножечко не так.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0116 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Как же все это было не вовремя!
- current normalized: Как же всё это было не вовремя!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0118 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: С одной стороны, все было совершенно неправильно.
- current normalized: С одной стороны, все было совершенно неправильно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0024-p-0120 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Довольно сложно организовать, а потом и «поддерживать» заготовленное место для конфиденциальной деловой встречи.
- current normalized: Довольно сложно организовать, а пот+ом и «поддерживать» заготовленное место для конфиденциальной деловой встречи.
- current rule: `phrase.potom`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0003 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки заслужил Ромка свой позывной.
- current normalized: Всё-таки заслужил Ромка свой позывной.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0014 / `СИБ`
- class: СВУ/СИБ; verdict: **UNRESOLVED**
- FB2 sentence: Тем более, коллеги были явно уверены, что их юному товарищу что-то угрожает на полигоне СИБ.
- current normalized: Тем более, коллеги были явно уверены, что их юному товарищу что-то угрожает на полигоне СИБ.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0016 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все, кому в тот момент не лень было, перегнулись через борт.
- current normalized: Все, кому в тот момент не лень было, перегнулись через борт.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0017 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И да, вы все не правы.
- current normalized: И да, вы все не правы.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0017 / `Не-е-е-е`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Не-е-е-е, — секунд через пять вынуждена была констатировать Тишь.
- current normalized: — Неее, — секунд через пять вынуждена была констатировать Тишь.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0019 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Меж тем в кузове все взгляды сошлись на застывшем в позе Будды психологе.
- current normalized: Меж тем в кузове все взгляды сошлись на застывшем в позе Будды психологе.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0019 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Тот в ответ на общее внимание чуть приоткрыл глаза.
- current normalized: Тот в ответ на общее внимание чуть приоткрыл глаза.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0021 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: Это потом в глазах современного западного обывателя, никакого отношения к «пути» не имеющего, смертельная наука превратилась театрализованное представление, мало пригодное в реальном бою.
- current normalized: Это потом в глазах современного западного обывателя, никакого отношения к «пути» не имеющего, смертельная наука превратилась театрализованное представление, мало пригодное в реальном бою.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0021 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: Это потом в глазах современного западного обывателя, никакого отношения к «пути» не имеющего, смертельная наука превратилась театрализованное представление, мало пригодное в реальном бою.
- current normalized: Это потом в глазах современного западного обывателя, никакого отношения к «пути» не имеющего, смертельная наука превратилась театрализованное представление, мало пригодное в реальном бою.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0024 / `Ну-у-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну-у-у-у-у, — разочарованно протянула валькирия, пригорюнившись, но тут же переключилась на новый объект.
- current normalized: — Нууу, — разочарованно протянула валькирия, пригорюнившись, но тут же переключилась на новый объект.
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0026 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все, — сообщил Гладь ровно.
- current normalized: — Все, — сообщил Гладь ровно.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0031 / `Девочки-и-и-и`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Как поесть приготовить на выходе так «Девочки-и-и-и!
- current normalized: — Как поесть приготовить на выходе так «Девочкиии!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0034 / `Пи-и-и-и-ить`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Пи-и-и-и-ить, — с трудом выдавил Волконский.
- current normalized: — Пииить, — с трудом выдавил Волконский.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0038 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Забрали себе все, а нам бросили объедки!
- current normalized: Забрали себе все, а нам бросили объедки!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0040 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — В-все?
- current normalized: — В-все?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0043 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: — Но ни капли мысли в глазах, — констатировала Настя и, к огромному облегчению парня, покачала головой.
- current normalized: — Но ни капли мысли в глазах, — констатировала Настя и, к огромному облегчению парня, покачала головой.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0051 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Мутный глаза, слой пыли поверх кровоточащих ссадин (все-таки «прокатиться» за пикапом ему пару раз пришлось) и…
- current normalized: Мутный глаза, слой пыли поверх кровоточащих ссадин (всё-таки «прокатиться» за пикапом ему пару раз пришлось) и…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0051 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Мутный глаза, слой пыли поверх кровоточащих ссадин (все-таки «прокатиться» за пикапом ему пару раз пришлось) и…
- current normalized: Мутный глаза, слой пыли поверх кровоточащих ссадин (всё-таки «прокатиться» за пикапом ему пару раз пришлось) и…
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0058 / `много-о-о`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: У меня дел еще много-о-о!..
- current normalized: У меня дел еще многооо!..
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0059 / `Та-а-а-ак`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Та-а-а-ак, — протянул парень негромко.
- current normalized: — Тааак, — протянул парень негромко.
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0025-p-0063 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Три часа, — уверенно ответила аналитик класса «Сигма», что значило одно из двух: либо она сейчас и впрямь СИЛЬНО занята, либо именно этому вопросу собирается уделить все свое внимание и проработать его очень глубоко.
- current normalized: — Три часа, — уверенно ответила аналитик класса «Сигма», что значило одно из двух: либо она сейчас и впрямь СИЛЬНО занята, либо именно этому вопросу собирается уделить все свое внимание и проработать его очень глубоко.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0004 / `не-е-е-е`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Не-не-не-не-не-е-е-е!
- current normalized: — Не-не-не-не-неее!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0010 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — Все хорошо, Саш?
- current normalized: — Все хорошо, Саш?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0011 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «И все это искренне!
- current normalized: «И всё это искренне!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0011 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: Веселости в глазах подруги не осталось и следа.
- current normalized: Веселости в глазах подруги не осталось и следа.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0015 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки коллеги «поддержали» его очень качественно.
- current normalized: Всё-таки коллеги «поддержали» его очень качественно.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0016 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — все же решил спародировать удивление он.
- current normalized: — всё же решил спародировать удивление он.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0017 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Отец решил, что поделиться тремя процентами акций Павлу будет куда дешевле, чем отдать Архиповым все.
- current normalized: Отец решил, что поделиться тремя процентами акций Павлу будет куда дешевле, чем отдать Архиповым все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0018 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: » — емкое определение буквально вынесло из головы девушки все лишние мысли.
- current normalized: » — емкое определение буквально вынесло из головы девушки все лишние мысли.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0018 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: В такой ситуации оставалось лишь порадоваться, что крепкая троечка прикрыта пусть и не самыми плотными, но все же кружевами.
- current normalized: В такой ситуации оставалось лишь порадоваться, что крепкая троечка прикрыта пусть и не самыми плотными, но всё же кружевами.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0022 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: «Ой, все!
- current normalized: «Ой, все!
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0025 / `Приве-е-е-е-ет`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Приве-е-е-е-ет!
- current normalized: — Привееет!
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0041 / `Ну-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну-у-у-у, — деланно нахмурилась Лика и, к ужасу подружки, картинно ударила кулачком в грудь молодого человека.
- current normalized: — Нууу, — деланно нахмурилась Лика и, к ужасу подружки, картинно ударила кулачком в грудь молодого человека.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0043 / `стены`
- class: стены; verdict: **OK**
- FB2 sentence: — Эх, то есть, ее голова не украсит стены моего замка?
- current normalized: — Эх, то есть, ее голова не украсит стены моего замка?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0045 / `Аа-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Аа-а-а-а, молодой господин, — слово «господин» телеведущая выдала в своем неповторимом стиле, обезоруживающе улыбнувшись.
- current normalized: — ААА, молодой господин, — слово «господин» телеведущая выдала в своем неповторимом стиле, обезоруживающе улыбнувшись.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0046 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — уже вполне сознательно и четко произнесла Саша, мыслено махнув рукой на все последствия.
- current normalized: — уже вполне сознательно и четко произнесла Саша, мыслено махнув рукой на все последствия.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0070 / `обреченно`
- class: обречённо; verdict: **OK**
- FB2 sentence: Мышкина обреченно покосилась на так и невскрытый конверт.
- current normalized: Мышкина обречённо покосилась на так и невскрытый конверт.
- current rule: `lexicon.project`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0078 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Правда, делиться информацией об очередном «заказе» все равно бы не стала.
- current normalized: Правда, делиться информацией об очередном «заказе» всё равно бы не стала.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0078 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки профессиональная этика, да и в мире серьезных людей любители почесать языком долго не живут.
- current normalized: Всё-таки профессиональная этика, да и в мире серьезных людей любители почесать языком долго не живут.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0079 / `Пу-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Пу-у-у-у-пу-пу-пу-пу-у-у-у…
- current normalized: — Пууу-пу-пу-пу-пууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0079 / `пу-у-у-у`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Пу-у-у-у-пу-пу-пу-пу-у-у-у…
- current normalized: — Пууу-пу-пу-пу-пууу…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0080 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Естественно, она не стала изучать все.
- current normalized: Естественно, она не стала изучать все.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0026-p-0080 / `глазками`
- class: глаза; verdict: **OK**
- FB2 sentence: Но глазками она пробежалась по нескольким листам, безошибочно отыскав страницу с тезисами.
- current normalized: Но глазками она пробежалась по нескольким листам, безошибочно отыскав страницу с тезисами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0004 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки раньше он не решался и взгляд задержать на обтянутых белыми форменными рубашечками прелестях.
- current normalized: Всё-таки раньше он не решался и взгляд задержать на обтянутых белыми форменными рубашечками прелестях.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0004 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: А если такие мысли и возникали (все же хороши были обе, чертовки!
- current normalized: А если такие мысли и возникали (вс+е же хороши были обе, чертовки!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0006 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Паутов, все еще впечатленный благосклонностью все также откровенно разглядывающих его сестричек, только кивнул одному из старых приятелей.
- current normalized: Паутов, всё еще впечатленный благосклонностью все также откровенно разглядывающих его сестричек, только кивнул одному из старых приятелей.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0006 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Паутов, все еще впечатленный благосклонностью все также откровенно разглядывающих его сестричек, только кивнул одному из старых приятелей.
- current normalized: Паутов, всё еще впечатленный благосклонностью все также откровенно разглядывающих его сестричек, только кивнул одному из старых приятелей.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0009 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Будущий жених самой Кошкиной (о чем он в своей компании давно растрепал всем, кому не лень было по десятому разу выслушивать эту все больше обрастающую интимными подробностями историю) недоуменно оглянулся на лысого крепыша, в его личной «гвардии» исполнявшего роль одного из «ближников».
- current normalized: Будущий жених самой Кошкиной (о чем он в своей компании давно растрепал всем, кому не лень было по десятому разу выслушивать эту всё больше обрастающую интимными подробностями историю) недоуменно оглянулся на лысого крепыша, в его личной «гвардии» исполнявшего роль одного из «ближников».
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0018 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: И все равно, остаться незамеченным не получилось.
- current normalized: И всё равно, остаться незамеченным не получилось.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0023 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Ну куда его отцу, бизнесмену средней руки, ссориться с хоть и очень-очень слабеньким по общим меркам, а все-таки кланом!
- current normalized: Ну куда его отцу, бизнесмену средней руки, ссориться с хоть и очень-очень слабеньким по общим меркам, а всё-таки кланом!
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0023 / `потом`
- class: потом; verdict: **OK**
- FB2 sentence: И ведь ничего потом не предпринять.
- current normalized: И ведь ничего потом не предпринять.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0026 / `А-а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — А-а-а-а…
- current normalized: — ААА…
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0038 / `Ма-а-а-акс`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ма-а-а-акс, — нескрываемым раздражением протянул клановец.
- current normalized: — Мааакс, — нескрываемым раздражением протянул клановец.
- current rule: `prosody.expressive_vowel_v3`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0042 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Такое выражение лица Макс уже видел.
- current normalized: Такое выражение лица Макс уже видел.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0043 / `стену`
- class: стены; verdict: **OK**
- FB2 sentence: — резко выкрикнул тот и запустил гаджет в стену.
- current normalized: — резко выкрикнул тот и запустил гаджет в стену.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0053 / `а-а-а`
- class: expressive elongation; verdict: **UNRESOLVED**
- FB2 sentence: — Ну, с*-*-*-*-*а-а-а…
- current normalized: — протянула он и с неожиданной даже для самого себя злостью припечатал.
- current rule: `prosody.expressive_vowel_v3, silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0068 / `Родов`
- class: родов; verdict: **OK**
- FB2 sentence: Просто упоминание новости со ссылкой на материл «Вестника РИ» (были опубликованы за час до блога), в котором рассматривалась бизнес-модель Паутовых: брать в жены представительниц знатных Родов для усиления собственных предприятий.
- current normalized: Просто упоминание новости со ссылкой на материл «Вестника РИ» (были опубликованы за час до блога), в котором рассматривалась бизнес-модель Паутовых: брать в жены представительниц знатных Родов для усиления собственных предприятий.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0068 / `лица`
- class: лица; verdict: **OK**
- FB2 sentence: Разве что шантаж Кошкиных, от лица которых выступила Лена…
- current normalized: Разве что шантаж Кошкиных, от лица которых выступила Лена…
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0077 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Отбросив все условности, она без всякого стеснения сделала солидный глоток.
- current normalized: Отбросив все условности, она без всякого стеснения сделала солидный глоток.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0083 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: — У тебя все готово?
- current normalized: — У тебя все готово?
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0087 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Очень уж ей хотелось увидеть все своими глазами.
- current normalized: Очень уж ей хотелось увидеть все своими глазами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0087 / `глазами`
- class: глаза; verdict: **OK**
- FB2 sentence: Очень уж ей хотелось увидеть все своими глазами.
- current normalized: Очень уж ей хотелось увидеть все своими глазами.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0093 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: За время поездки (кстати, тщательно рассчитанное все той же Светланой в паре с Викторией) он успел завести себя, но вот подключить к решению проблемы разум еще нет.
- current normalized: За время поездки (кстати, тщательно рассчитанное все той же Светланой в паре с Викторией) он успел завести себя, но вот подключить к решению проблемы разум еще нет.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0095 / `Все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Все-таки тренирован он был относительно неплохо.
- current normalized: Всё-таки тренирован он был относительно неплохо.
- current rule: `silero.preprocessing`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0096 / `глаза`
- class: глаза; verdict: **OK**
- FB2 sentence: Кошкина краем глаза наблюдала за едва заметно улыбнувшимся Павлом.
- current normalized: Кошкина краем глаза наблюдала за едва заметно улыбнувшимся Павлом.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0027-p-0102 / `глазах`
- class: глаза; verdict: **OK**
- FB2 sentence: Свет под хруст зубов погас в глазах Паутова гораздо раньше,чем он успел осознать НА КОГО именно напал.
- current normalized: Свет под хруст зубов погас в глазах Паутова гораздо раньше,чем он успел осознать НА КОГО именно напал.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0028-p-0009 / `замок`
- class: замок; verdict: **OK**
- FB2 sentence: Оно мало походило на артефактный ключ, но замок послушно отозвался тоновым сигналом.
- current normalized: Оно мало походило на артефактный ключ, но зам+ок послушно отозвался тоновым сигналом.
- current rule: `phrase.lock_after_key`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0028-p-0010 / `все`
- class: все/всё; verdict: **OK**
- FB2 sentence: Хотя, если быть честным, именно перед этим «гостем» были отрыты едва ли не все двери империи.
- current normalized: Хотя, если быть честным, именно перед этим «гостем» были отрыты едва ли не все двери империи.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0028-p-0011 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: А в прошлый раз времени изучить «наскальную» живопись на стенах не было.
- current normalized: А в прошлый раз времени изучить «наскальную» живопись на стенах не было.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required

### Book 10 / ch-0028-p-0023 / `стенах`
- class: стены; verdict: **OK**
- FB2 sentence: Цесаревич в этих стенах хранил инкогнито.
- current normalized: Цесаревич в этих стенах хранил инкогнито.
- current rule: `none`
- approximate MP3: None s; clip: `None`
- negative controls: manual corpus review required
