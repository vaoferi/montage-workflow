# Відновлення аудіо (restoration pipeline)

Джерело: матеріал №5 (`knowledge/inbox/2026-11-21-audio-restoration-advisory.md`), отримано 2026-11-21. Статус: active.
Застосовність: будь-який монтаж із проблемним звуком.

## Принцип

Не шукати один чарівний denoiser. Потрібна комбінація: **target speaker extraction → speech separation → enhancement**.

Задача — не стерильний запис, а врятовані реальні слова. Краще трохи гірший звук із реальною фразою, ніж ідеальний AI-голос, який сказав те, чого людина не казала. Speech fidelity — `process/agent-discipline.md`.

## Torture test (обов'язково перед batch)

1. Знайти 30–60 с найпроблемнішого фрагмента: тихий цільовий голос + environmental noise + сторонній speaker (якщо є).
2. Зберегти `audio_test/00_original.wav`: 48 kHz PCM, без destructive normalization.
3. Прогнати кандидатів-матрицю: original; speech enhancement; separation stems; AV target speaker extraction для кожного цільового мовця; DeepFilterNet; SepFormer; Resemble denoise; Resemble full (experimental).
4. Слухати **1 хвилину × N варіантів**, а не весь матеріал × N.
5. Зафіксувати результати; лише потім масштабувати переможців на матеріал.

Після torture test не обробляти весь матеріал автоматично — спершу визначити, який pipeline має сенс масштабувати.

## Порядок інструментів

1. **AV target speaker extraction** (коли видно обличчя/губи) — найвищий пріоритет. Модель дивиться на lip/face cue і дістає голос конкретної людини; потенційно прибирає оператора, сторонніх і частину шуму.
2. **Speech separation** (коли обличчя не видно або кілька голосів) — окремі stems; визначати, хто є хто, за слухом + відео + транскриптом, не припускати автоматично.
3. **Speech enhancement** — після extraction/separation або як самостійний варіант.
4. **DeepFilterNet** — консервативний робочий кінь; до separation (якщо шум заважає моделі) або після (якщо голос ще шумний), але не обидва без потреби: подвійний denoise перетворює голос на «MP3 із 2003-го».
5. **Resemble Enhance**: `--denoise_only` — широко; full enhance — лише найгірші фрази, EXPERIMENTAL, з обов'язковим порівнянням transcript.
6. **Adobe Enhance Speech v2** — сильний one-click enhancer (noise, reverb, chatter, music), але **не** speaker extractor: сторонній оператор теж говорить людським голосом.
7. **ElevenLabs / Auphonic** — benchmark-и: ElevenLabs на найгірших хвилинах; Auphonic free має jingle → не в основний пайплайн.

Довідка моделей і актуальних лімітів — `tools/audio-models.md` (version-sensitive, перевіряти перед використанням).

## Pipeline-приклад (target speaker)

CAMERA VIDEO+AUDIO → AV TSE (16 kHz) → speech super-resolution 48k → легкий cleanup (DeepFilterNet / NLE cleanup) → EQ + compression + room tone → NLE.

Для кількох мовців — окремі cleaned tracks, зібрані назад по таймкодах. Не намагатися одним denoiser'ом врятувати весь soundtrack.

## Перевірка кожного кандидата

- потрібний speaker залишився;
- сторонні speakers прибрані;
- слова не втрачено;
- немає pumping / metallic artifacts;
- super-resolution: A/B 16k vs SR 48k, не приймати автоматично.

## Transcript consensus

Протранскрибувати original і кандидатів, порівняти слова.

- Cleaned-версії стабільно розпізнають слова, яких original не дав → позитивний сигнал.
- Кандидат видає слова, яких немає в інших → `POSSIBLE_AI_SPEECH_ARTIFACT`, без manual review не використовувати.
- Суттєва розбіжність transcript-ів → `MANUAL_REVIEW`.

## Report

Папка `audio_test/candidates/`; усі кандидати синхронізовані до однакового start time і duration.

Таблиця: `candidate | noise removal | target intelligibility | other speakers removed | naturalness | artifacts | transcript confidence`.

- Не обирати переможця лише за автоматичною метрикою.
- Не вигадувати оцінки для кандидатів, які реально не прослухані.
- Відзначити: найкращий варіант для кожного цільового мовця; найкращий conservative cleanup; найкращий aggressive rescue.

## Обмеження

- Не тренувати нові моделі.
- Не запускати TSE сліпо, якщо обличчя/губи не видно достатньо добре.
- Не робити double-denoise, якщо він створює артефакти.
- Full enhance не стає production audio автоматично.
