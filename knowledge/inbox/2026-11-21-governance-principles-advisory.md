Так, тут є що перенести. Я прочитав `vaoferi/vaoferi-start-here`, зокрема **`AGENTS.md`**, **`PROJECT_RULES.md`**, `vaoferi-bootstrap`, `vaoferi-engineering`, `vaoferi-project-adaptation` і `vaoferi-dependencies`.

І твоя нинішня система насправді **дуже добре лягає на AI-відеомонтаж**.

### Що я точно переніс би

- **80/20** → спочатку історія, критичний звук, ключові моменти й найбільші дефекти; потім полірування.
- **Root cause, а не симптом** → не просто стабілізувати поганий рух, а знайти чисту частину кадру / перекомпонувати / замінити B-roll.
- **Native capability before new dependency** → перед установкою чергової AI-моделі перевіряти, чи Resolve Studio вже робить це нормально.
- **`Done = verified`** → ролик не готовий, поки його реально не переглянуто, звук не прослухано, проблемні місця не перевірено.
- **Не вигадувати результати** → агент не має писати “аудіо очищено” лише тому, що команда завершилась без error.
- **Version-sensitive → current docs** → DaVinci/API/моделі перевіряти за актуальними версіями.
- **Мінімальна достатня зміна** → не пропускати весь фільм через enhancement, якщо проблема в 12 кліпах.
- **Не робити global replace без target review** → це прямо золото для відео: не застосовувати NR, stabilization, LUT, voice enhancement тощо до всього матеріалу без тестового фрагмента.
- **Small safe change / risky architectural change** → поправити один кліп ≠ змінити весь audio pipeline.
- **Inventory → classify → conflicts → migrate → verify** із `project-adaptation` → фактично ідеальний workflow для розбору сирого весільного матеріалу.
- **Якщо бачиш сусідню проблему — повідом** → наприклад, агент займається шумом, але бачить clipping, неправильний fps або desync — не мовчить.
- **Не питати власника те, що можна встановити самому** → агент сам читає metadata, codecs, fps, resolution, tracks, Resolve project settings.

Але найважливіше: у твоєму `Start Here` прямо закладено, що **project-specific правила не мають жити в універсальному `AGENTS.md`**.

Тому для цього проєкту я б зробив:

```text
AGENTS.md
    універсальний Vaoferi-контракт

PROJECT_RULES.md
    конкретні правила цього wedding-проєкту

docs/VIDEO_EDITING.md
    детальна редакторська доктрина, яку ми вже зібрали

docs/AUDIO_PIPELINE.md
    Resolve / DeepFilterNet / ClearVoice / WhisperX тощо
```

Тобто `AGENTS.md` залишається компактним мозком агента, а не енциклопедією туфель нареченого.

## 1. Оцей prompt я б дав агенту зараз

Підготуй цей video-editing repository/project до довготривалої автономної роботи AI-агента за моїм стандартом Vaoferi.

Canonical source моїх універсальних правил:

GitHub:
vaoferi/vaoferi-start-here

Перед будь-якими змінами прочитай актуальні:

- `AGENTS.md`
- `PROJECT_RULES.md`
- `.agents/skills/vaoferi-bootstrap/SKILL.md`
- `.agents/skills/vaoferi-engineering/SKILL.md`
- `.agents/skills/vaoferi-project-adaptation/SKILL.md`
- `.agents/skills/vaoferi-dependencies/SKILL.md`

Якщо canonical bootstrap/sync mechanism із `vaoferi-start-here` доступний і придатний для цього repository, віддай перевагу йому замість ручного копіювання.

КРИТИЧНО:

Не перетворюй universal `AGENTS.md` на файл правил конкретного wedding project.

Архітектура повинна залишатися:

`AGENTS.md`
= універсальний Vaoferi owner/agent contract.

`PROJECT_RULES.md`
= hard constraints, source-of-truth та специфіка саме цього video project.

`docs/VIDEO_EDITING.md`
= детальні творчі, монтажні й QC правила.

`docs/AUDIO_PIPELINE.md`
= детальний audio restoration / transcription / mixing pipeline, якщо матеріалу достатньо для окремого документа.

Якщо в цьому project уже існують правила, prompts, docs, scripts, transcripts, analysis results або інший накопичений контекст:

НЕ перезаписуй їх навмання.

Застосуй принцип:

inventory
→ classify
→ conflicts
→ migrate
→ parity
→ cleanup
→ verify.

Не втрать жодної унікальної корисної домовленості.

---

## PROJECT-SPECIFIC PRINCIPLES

У `PROJECT_RULES.md` зафіксуй щонайменше такі правила.

### 1. Primary outcome

Мета — створити максимально якісний wedding film із технічно нерівного або слабко знятого вихідного матеріалу.

Оптимізуй:

story
→ emotion
→ intelligibility
→ continuity
→ visual quality
→ cinematic polish.

Не оптимізуй кількість використаного footage.

Велика частина сирого матеріалу може бути відкинута.

### 2. Originals are immutable

Original camera/media/audio files вважай READ-ONLY source of truth.

Не:

- перезаписуй;
- перекодовуй поверх originals;
- перейменовуй масово без потреби;
- видаляй;
- destructive-trim;
- destructive-normalize.

AI/generated/restored/proxy/transcoded assets зберігай окремо з provenance до original source.

Будь-яка destructive або irreversible operation потребує окремого дозволу.

### 3. Evidence before Done

`Done` означає перевірений результат.

У цьому project успішне виконання CLI command, Python script, Resolve API call або AI model inference НЕ є доказом якісного результату.

Рівень verification має відповідати ризику.

Наприклад:

audio restoration
→ прослухати A/B та перевірити intelligibility/artifacts;

video denoise
→ переглянути 100% crop + motion;

stabilization
→ перевірити весь processed shot на warp/crop;

color
→ scopes + skin + сусідні shots;

rough cut
→ перегляд sequence в реальному часі;

final
→ повний QC render.

Не повідомляй “успішно покращено”, якщо перевірено лише exit code.

### 4. Test before batch

Ніколи не застосовуй дорогий, destructive-looking або AI-heavy processing до всього матеріалу лише тому, що він добре спрацював на одному shot.

Перед batch:

1. визнач problem class;
2. вибери representative difficult sample;
3. створи processed candidate;
4. зроби A/B comparison;
5. перевір artifacts;
6. лише після цього масштабуй на відповідну групу clips.

Не роби global replacement без reviewed target list.

### 5. Native before dependency

Перед установкою нового tool/model перевір:

1. чи проблема взагалі потребує processing;
2. чи її можна вирішити правильним edit;
3. чи її вже якісно вирішує DaVinci Resolve Studio;
4. чи існуючий installed tool уже це покриває;
5. чи сторонній інструмент дає суттєве покращення.

Не додавай dependency заради технологічної цікавості.

### 6. Root cause before cosmetic fix

Виправляй причину проблеми, коли це пропорційно.

Приклад:

поганий 8-second camera movement

не означає:

“стабілізувати всі 8 секунд”.

Спочатку перевір:

- чи потрібен весь shot;
- чи є 1–2 секунди чистого моменту;
- чи можна обрізати;
- чи є альтернативний angle;
- чи можна закрити B-roll;
- чи можна stabilize + reframe;
- лише потім використовуй складний restoration.

### 7. Proportional work

Використовуй 80/20.

Спочатку:

- ключові wedding moments;
- intelligibility vows/speeches;
- story;
- найсильніші reactions;
- критичні технічні дефекти;
- continuity.

Потім:

- polishing;
- micro-animation;
- secondary B-roll;
- дрібний cleanup.

Не витрачай годину на restoration decorative shoe shot, якщо погано чути vows.

### 8. Neighboring problems

Якщо під час виконання задачі виявлена сусідня проблема, що суттєво впливає на фінальну якість, не ігноруй її.

Наприклад:

- clipping;
- wrong color transform;
- fps mismatch;
- audio drift;
- missing channel;
- incorrect sync;
- corrupted media;
- focus issue;
- duplicated shot;
- inconsistent white balance.

Коротко зафіксуй:

problem
→ impact
→ recommendation.

Не розширюй scope мовчки до повного переписування pipeline.

### 9. Current information

Version-sensitive речі перевіряй за актуальними джерелами:

- DaVinci Resolve Studio;
- Resolve scripting API;
- FFmpeg;
- Whisper/faster-whisper/WhisperX;
- DeepFilterNet;
- ClearVoice;
- pyannote;
- AI restoration tools;
- codecs;
- dependencies.

Не покладайся на старий syntax або старі capabilities, якщо вони могли змінитися.

### 10. Autonomous discovery

Не питай мене про те, що можеш встановити сам.

Перед питанням перевір:

- files;
- metadata;
- codecs;
- resolution;
- FPS;
- timestamps;
- audio channels;
- waveform;
- transcripts;
- Resolve project;
- existing scripts;
- logs;
- generated reports;
- previous analysis.

Запитуй мене лише про:

- творчий preference;
- суперечливу інтерпретацію;
- справжню business/quality priority;
- missing fact, якого немає у project.

### 11. Prefer reversible workflows

Віддавай перевагу:

markers;
metadata;
sidecar JSON;
derived assets;
new timelines;
versions;
Resolve duplicate timelines;
non-destructive grades;
separate audio tracks;

замість незворотної модифікації source.

Для riskier processing завжди май rollback path.

### 12. Preserve provenance

Для externally processed assets має бути зрозуміло:

original source;
tool/model;
settings;
version;
processing purpose;
output file.

Не допускай ситуації, коли через тиждень неможливо зрозуміти, звідки взявся `audio_final_final2_clean.wav`.

### 13. Human review gates

AI може автономно:

analyze;
rank;
transcribe;
create selects;
create candidate restoration;
create markers;
build rough cut candidates;
prepare A/B comparisons.

Але важливі irreversible або quality-sensitive рішення повинні мати evidence.

Особливо:

- reconstructed speech;
- aggressive enhancement;
- AI interpolation;
- heavy denoise;
- face/detail reconstruction;
- final color;
- final story cut.

### 14. Speech fidelity

Для vows, speeches, pastor/officiant та інших реальних висловлювань:

не допускай AI-процес, який може непомітно змінити фактичні слова.

Enhancement ≠ permission to invent speech.

Якщо різні transcripts суттєво розходяться:

mark `MANUAL_REVIEW`.

Не вигадуй найбільш правдоподібний текст.

### 15. Source of truth

Не підтримуй кілька суперечливих джерел правил.

`AGENTS.md`
→ universal behavior.

`PROJECT_RULES.md`
→ project invariants.

`docs/VIDEO_EDITING.md`
→ editing doctrine.

`docs/AUDIO_PIPELINE.md`
→ audio workflow.

Current Resolve project/timelines/media
→ фактичний editing state.

Якщо старий prompt суперечить canonical current rules, не залишай обидва активними.

---

## ADAPT ENGINEERING PRINCIPLES TO MEDIA

Перенеси корисну логіку Vaoferi Engineering на video workflow.

Аналог TDD для media-processing:

problem sample
→ baseline evidence
→ minimal candidate processing
→ A/B verification
→ apply to target class
→ regression/QC check.

Не видаляй baseline/original лише тому, що новий processed result виглядає кращим.

Не ослаблюй QC criterion лише щоб processing вважався “успішним”.

---

## OUTPUT

Після discovery:

1. створи/синхронізуй `AGENTS.md` правильно;
2. створи або акуратно доповни `PROJECT_RULES.md`;
3. перенеси детальні існуючі монтажні правила в `docs/VIDEO_EDITING.md`;
4. перенеси audio restoration/transcription rules у `docs/AUDIO_PIPELINE.md`, якщо це виправдано;
5. не дублюй однакові правила в чотирьох файлах;
6. перевір inbound references та структуру;
7. покажи мені короткий звіт:

- що створено;
- що мігровано;
- які правила були дублями;
- які конфлікти знайдено;
- що залишилось unresolved;
- які перевірки реально виконані.

Не називай setup завершеним лише тому, що файли створені.

Перевір, що наступний новий AI session, прочитавши `AGENTS.md` → `PROJECT_RULES.md` → routed project docs, реально отримає достатній контекст для продовження роботи без повторного пояснення всього проєкту.

## 2. А це я б дав **після створення файлів**, як self-review

Це непогано захищає від класичного агентського “я створив 900 рядків документації, отже я продуктивний”.

Проведи governance review цього video-editing project.

Не змінюй файли на першому проході.

Прочитай:

- `AGENTS.md`
- `PROJECT_RULES.md`
- `docs/VIDEO_EDITING.md`
- `docs/AUDIO_PIPELINE.md`
- інші active AI instructions / prompts / rules у repository.

Порівняй їх з canonical principles `vaoferi/vaoferi-start-here`.

Перевір:

1. Чи `AGENTS.md` залишився universal, а не перетворився на video-specific encyclopedia.
2. Чи project-specific факти знаходяться у `PROJECT_RULES.md` або project-owned docs.
3. Чи немає дублювання active rules.
4. Чи немає суперечностей.
5. Чи original media чітко захищені від destructive changes.
6. Чи `Done` вимагає реального verification.
7. Чи batch AI-processing має sample/A-B gate.
8. Чи agent спочатку перевіряє Resolve/native capability перед встановленням нових dependencies.
9. Чи speech restoration не може непомітно підміняти реальні слова.
10. Чи processing results мають provenance та rollback path.
11. Чи subjective editing judgement не намагаються machine-enforce дурними brittle checks.
12. Чи objective invariants, навпаки, можна перевіряти автоматично.
13. Чи наступна AI session однозначно зрозуміє:
   - де source of truth;
   - що можна змінювати;
   - що не можна;
   - як перевіряти результат;
   - де лежить editing doctrine;
   - де лежить audio pipeline.
14. Чи існуючі важливі правила цього wedding project не були втрачені під час cleanup.

Для кожної проблеми дай:

`source → problem → impact → recommended destination/fix`.

Після analysis зроби лише мінімальні необхідні виправлення.

Не переписуй документацію заради стилю.

Не збільшуй `AGENTS.md`, якщо правило можна правильно маршрутизувати в project-owned documentation.

Наприкінці покажи:

- changed files;
- які governance problems виправлені;
- що залишилося unresolved;
- як перевірено, що не втрачено project knowledge.

### Ще одна штука, яку я б додав пізніше

У твоєму `Start Here` є дуже хороша думка: **об'єктивне правило краще зробити machine-enforceable, ніж сто разів написати в Markdown**.

Для цього проєкту агент згодом може зробити невеликий `scripts/project_check.py`, який автоматично перевіряє, наприклад:

```text
- originals не лежать у generated/output folders
- немає overwrite source paths
- derived audio має provenance
- transcript існує для analyzed speech
- output не має missing media
- expected FPS / timeline resolution правильні
- final audio не clipping
- generated assets не загубили source mapping
```

А от **“кадр красивий”, “ритм достатньо емоційний”, “цей push-in доречний”** автоматичним hard-rule робити не треба. У твоєму `project-adaptation` це теж прямо добре сформульовано: суб'єктивний judgement не треба перетворювати на крихкий машинний тест.

Із усього, що я прочитав у `vaoferi-start-here`, саме **`Done = evidence` + `test before batch` + `root cause` + чітке розділення universal/project rules** я вважаю найціннішими для цієї третьої спроби монтажу. Вони якраз лікують типову хворобу AI-агента: багато activity, зелений `success`, а ролик усе ще лайно. 😄