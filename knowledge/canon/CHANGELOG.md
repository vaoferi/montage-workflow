# CHANGELOG канону

## 2026-11-21 — матеріал №7 (бриф оркестратора)

Джерело: `knowledge/inbox/2026-11-21-orchestrator-skill-brief.md` (бриф власника, отримано 2026-11-21).

Зміни канону:

- `qc/qc-protocol.md` — додано «Фінальні заборони (жорстко)»: обрізані думки (лише за явним запитом користувача), обрізані голови/кінцівки фраз, очевидний шлак (повтори, оговорки, єкання/бекання, порожні паузи, чорні кадри, невмотивовані стрибки). Кожен випадок фіксується і виправляється до оголошення результату.

Поза каноном: створено скіл-оркестратор `skills/montage-director/` (маршрут для дилетантів: doctor → обсяг → інвентар → транскрипція → маркування шлаку → інтерв'ю → сценарій → монтаж → редактор → QC).

Конфлікти: немає. Superseded: немає.

## 2026-11-21 — матеріал №6

Джерело: `knowledge/inbox/2026-11-21-external-skills-advisory.md` (отримано 2026-11-21).

Додано:

- `tools/skill-repos.md` — реєстр зовнішніх Agent Skills для відеопродакшену з перевіркою існування репо станом на 2026-11-21 (9 репо, усі public) + обов'язкова політика: автооновлення з офіційних репо перед застосуванням, фіксація commit SHA, огляд змін, мінімальний набір, smoke test на реальному фрагменті, перегляд результату зі звуком, лише офіційні джерела.

Вказівка власника: скіли мають стати частиною воркфлоу, але з автооновленням з офіційних репо перед застосуванням у роботі.

Оновлено: `process/agent-discipline.md` — зовнішні скіли явно визнано залежностями з посиланням на політику.

Конфлікти: немає. Superseded: немає.

## 2026-11-21 — матеріал №5

Джерело: `knowledge/inbox/2026-11-21-audio-restoration-advisory.md` (отримано 2026-11-21).

Додано:

- `audio/restoration-pipeline.md` — метод відновлення звуку: комбінація target speaker extraction → separation → enhancement; обов'язковий torture test (30–60 с, матриця кандидатів, 1 хв × N замість усього матеріалу × N); порядок інструментів; pipeline-приклад AV TSE → SR 48k → cleanup → EQ/compression; перевірка кандидатів (speakers, слова, pumping/metallic); transcript consensus (`POSSIBLE_AI_SPEECH_ARTIFACT`, `MANUAL_REVIEW`); report-таблиця; обмеження.
- `tools/audio-models.md` — version-sensitive довідка: ClearerVoice (SE 48K, SS 16K, AV TSE 16K, SR 48K), Adobe Enhance Speech v2 (ліміти free), DeepFilterNet, SpeechBrain SepFormer-WHAM, Resemble Enhance, ElevenLabs Voice Isolator, Auphonic.

Оновлено: `audio/audio-priority.md` — cross-ref на пайплайн; `knowledge/domains/wedding.md` — пріоритет рятування голосів нареченої/нареченого/ведучого.

Ключове правило матеріалу збережено: краще трохи гірший звук із реальною фразою, ніж ідеальний AI-голос, що сказав те, чого людина не казала.

Конфлікти: немає. Superseded: немає.

## 2026-11-21 — матеріал №4 (два підходи → золота середина)

Джерела: `knowledge/inbox/2026-11-21-shot-composition-soft.md` (м'якший підхід: rescue-first, 40 правил) і `knowledge/inbox/2026-11-21-shot-composition-strict.md` (жорсткіший: кожен кадр навмисно скомпонований, 38 правил). Вказівка власника: «підбери мудро золоту середину».

Синтез у `style/shot-composition.md`:

- **М'яка політика відбору** (від soft-підходу): низька якість/композиція сама по собі не є критерієм відбракування; кадр відкидається лише коли надлишковий/непридатний без унікальної story-coverage цінності; remove-тест: нічого не додає + є краща альтернатива + більше проблем, ніж користі.
- **Жорсткий стандарт виконання** (від strict-підходу): кожен використаний кадр виглядає навмисно; відповідь на «куди глядач має дивитися?» обов'язкова; safe face crop (не через очі/рот/підборіддя), не різати по суглобах, чисті краї, контроль горизонту, різноманіття крупностей, пастка «вакууму з двох облич».
- Зведені: три питання перед кожним crop; правила побудови як цілі, не фільтр; єдина rescue-процедура (17 кроків); scoring як інструмент вибору, не delete-threshold; мінімальне покриття сцени; стратегія для слабкої сцени цілком; final composition QC.

Обидва сирі варіанти збережено в inbox без змін. Конфлікти: підходи відрізнялися політикою відбракування — розв'язано явно (політика м'яка, виконання жорстке). Superseded: немає.

## 2026-11-21 — матеріал №3

Джерело: `knowledge/inbox/2026-11-21-governance-principles-advisory.md` (отримано 2026-11-21; перенесення інженерних принципів власника `vaoferi/vaoferi-start-here` на відеомонтаж; canonical repo перевірено — публічний, main).

Додано область `process/` (інженерна дисципліна агента, універсальна):

- `process/agent-discipline.md` — 80/20, root cause, native before dependency, мінімальна зміна, no global replace, inventory→classify→conflicts→migrate→verify, сусідні проблеми, автономне з'ясування, актуальність джерел, оригінали незмінні, зворотні workflow, provenance, людські гейти, speech fidelity, джерела правди без дублювання.
- `process/verification.md` — Done = evidence; рівні доказів під ризик (audio A/B, denoise crop, stabilization, color scopes, rough cut realtime, final QC); test before batch; media-TDD; об'єктивні інваріанти vs суб'єктивні судження; звітність.
- `process/governance-review.md` — чекліст із 14 перевірок інструкцій агента.

Оновлено крос-посилання: `qc/qc-protocol.md`, `audio/audio-priority.md` (speech fidelity), `style/analysis-method.md` (людські гейти), `knowledge/domains/wedding.md` (speech fidelity для vows/speeches).

Зафіксовано: canonical source універсальних правил — `vaoferi/vaoferi-start-here`; при побудові `AGENTS.md` віддавати перевагу його bootstrap/sync механізму.

Конфлікти: немає. Superseded: немає.

## 2026-11-21 — матеріал №2

Джерело: `knowledge/inbox/2026-11-21-controlled-dynamics-advisory.md` (отримано 2026-11-21 у чаті).

Додано:

- `style/controlled-dynamics.md` — принцип «перезнімання в постобробці»: digital push-in/pull-out, pan/reframe, stabilize→recreate, recomposition, fake second camera, motion continuity, match movement, cut on motion, керування швидкістю, мікродинаміка, фотографії, глибина, контраст ритму, заборона переобробки, практична драбина рятунку, вірність фінальному відео. Записано універсально, без доменної прив'язки.

Оновлено:

- `style/editing-grammar.md` — salvage посилається на повну драбину рятунку.
- `tools/resolve-21.md` — Transform keyframes, Dynamic Zoom, Speed Warp (режим Better), окремі контролі стабілізації.
- `knowledge/domains/wedding.md` — доменні акценти застосування прийомів.

Конфлікти: немає. Superseded: немає.

## 2026-11-21 — коригування №1: універсалізація

Вказівка власника: канон записується як універсальний, без орієнтації на весільний домен.

- Універсальні частини виділено з доменного файла в `style/analysis-method.md`: трипрохідний аналіз, інвентаризація, люди, сцени, технічні флаги, дублікати, класифікація, маркери, безпека автоматизації.
- Доменний файл переміщено `canon/domains/wedding/profile.md` → `knowledge/domains/wedding.md` (поза каноном; канон лишається універсальним, домени — окремий шар).
- Приклади в `style/editing-grammar.md` і `audio/audio-priority.md` узагальнено: без весільної лексики (туфлі/vows/dance → деталі, ключова мова, динамічні масові сцени).

## 2026-11-21 — матеріал №1

Джерело: `knowledge/inbox/2026-09-18-wedding-editorial-advisory.md` (отримано 2026-11-21; контент датований 2026-09-18; зовнішні посилання збережені в inbox).

Додано:

- `style/editing-grammar.md`
- `audio/audio-priority.md`
- `qc/qc-protocol.md`
- `domains/wedding/profile.md` (пізніше переміщено)
- `tools/resolve-21.md`

Розширення структури: додано категорію `tools/` (довідки про інструменти), якої не було в початковому переліку spec (`style/platform/audio/qc/delivery`).

Конфлікти: немає (перший матеріал). Superseded: немає.
