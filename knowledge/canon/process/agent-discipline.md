# Дисципліна агента: інженерні принципи для монтажу

Джерело: матеріал №3 (`knowledge/inbox/2026-11-21-governance-principles-advisory.md`), отримано 2026-11-21. Статус: active.
Застосовність: будь-який проєкт монтажу, будь-який агент.

Канонічне джерело універсальних правил власника: `vaoferi/vaoferi-start-here` (публічний, перевірено 2026-11-21). При побудові `AGENTS.md` віддавати перевагу наявному bootstrap/sync механізму, якщо він придатний.

## 80/20 — пропорційність роботи

Спочатку: ключові моменти; intelligibility ключової мови; історія; найсильніші реакції; критичні технічні дефекти; continuity.

Потім: полірування, micro-animation, другорядний B-roll, дрібний cleanup.

Не витрачати годину на restoration декоративного кадру, якщо погано чути ключові слова.

## Root cause, не симптом

Поганий 8-секундний рух ≠ «стабілізувати всі 8 секунд». Спершу перевірити: чи потрібен весь shot; чи є 1–2 секунди чистого моменту; чи можна обрізати; чи є альтернативний angle; чи можна закрити B-roll; чи допоможе stabilize + reframe; і лише потім — складна реставрація.

## Native capability before new dependency

Перед встановленням нового tool/model перевірити послідовно:

1. чи проблема взагалі потребує processing;
2. чи вирішується правильним edit;
3. чи вже якісно робить DaVinci Resolve Studio;
4. чи покриває наявний встановлений інструмент;
5. чи сторонній інструмент дає суттєве покращення.

Не додавати залежність заради технологічної цікавості.

## Мінімальна достатня зміна

Не проганяти весь фільм через enhancement, якщо проблема в 12 кліпах.

Розрізняти малий безпечний фікс (один кліп) і ризикову архітектурну зміну (весь audio pipeline) — і поводитися відповідно до масштабу.

## Жодних глобальних замін без переглянутого списку цілей

NR, stabilization, LUT, voice enhancement тощо — не застосовувати до всього матеріалу без тестового фрагмента. Деталі — `process/verification.md` (Test before batch).

## Inventory → classify → conflicts → migrate → verify

Для розбору сирого матеріалу і для будь-якої міграції/реорганізації: інвентаризація → класифікація → конфлікти → міграція → паритет → cleanup → верифікація.

Не втратити жодної унікальної корисної домовленості.

## Сусідні проблеми

Побачив суттєву сусідню проблему (clipping, неправильний color transform, fps mismatch, audio drift, відсутній канал, desync, пошкоджене медіа, focus issue, дублікат, inconsistent white balance) — коротко зафіксувати:

problem → impact → recommendation.

Не мовчати і не розширювати scope мовчки до переписування всього пайплайна.

## Автономне з'ясування

Не питати власника про те, що можна встановити самому. Перед питанням перевірити: files, metadata, codecs, resolution, FPS, timestamps, audio channels, waveform, transcripts, Resolve project, існуючі скрипти, logs, звіти, попередній аналіз.

Питати лише про: творчий preference; суперечливу інтерпретацію; справжній business/quality priority; відсутній факт, якого немає в проєкті.

## Актуальність інформації

Version-sensitive речі перевіряти за актуальними джерелами: DaVinci Resolve Studio, Resolve scripting API, FFmpeg, Whisper/faster-whisper/WhisperX, DeepFilterNet, ClearVoice, pyannote, AI restoration tools, codecs, dependencies. Не покладатися на старий синтаксис або старі capabilities.

## Оригінали незмінні

Original camera/media/audio files — READ-ONLY source of truth. Заборонено: перезаписувати, перекодовувати поверх, масово перейменовувати без потреби, видаляти, destructive-trim, destructive-normalize.

AI/generated/restored/proxy/transcoded assets зберігаються окремо з provenance до original source. Будь-яка destructive або irreversible операція — лише з окремим дозволом власника.

## Зворотні workflow

Перевага: markers, metadata, sidecar JSON, derived assets, нові timelines, versions, Resolve duplicate timelines, non-destructive grades, окремі audio tracks — замість незворотної зміни source.

Для ризикового processing — завжди rollback path.

## Provenance

Для externally processed assets має бути ясно: original source, tool/model, settings, version, processing purpose, output file. Через тиждень не повинно бути питання, звідки взявся `audio_final_final2_clean.wav`.

## Людські гейти

AI може автономно: analyze, rank, transcribe, створювати selects, candidate restoration, markers, rough cut candidates, A/B comparisons.

Evidence обов'язковий для: reconstructed speech, aggressive enhancement, AI interpolation, heavy denoise, face/detail reconstruction, final color, final story cut.

## Speech fidelity

Для реальних висловлювань жоден AI-процес не може непомітно змінювати фактичні слова. Enhancement ≠ дозвіл вигадувати мову.

Якщо різні transcripts суттєво розходяться — позначати `MANUAL_REVIEW`. Не вигадувати найбільш правдоподібний текст.

## Джерела правди без дублювання

Розділення рівнів:

- `AGENTS.md` — універсальна поведінка агента (компактний мозок, не енциклопедія);
- workflow-документація — етапи й гейти;
- `knowledge/canon/` — універсальні правила;
- `knowledge/domains/` — доменні інстанси;
- project-рівень — інваріанти конкретного проєкту;
- фактичний editing state — Resolve project/timelines/media.

Однакові правила не дублюються між файлами. Якщо старий prompt суперечить canonical current rules — не залишати обидва активними.
