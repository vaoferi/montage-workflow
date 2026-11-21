# Дизайн: montage-workflow — універсальний воркфлоу монтажу відео для ШІ-агентів

Дата: 2026-11-21
Статус: затверджено власником у чаті, очікує рев'ю файлу

## Мета

Портативний кросплатформний фреймворк монтажу відео, який:

1. Ініціалізується на будь-якому ПК (macOS, Linux, Windows) клонуванням репозиторію і одним bootstrap-скриптом.
2. Керується ШІ-агентами за єдиним канонічним пайплайном (`workflow/pipeline.yaml`).
3. Перетворює зібраний власником матеріал (нотатки, референси, приклади стилю, інструкції) на структуровані канонічні правила в `knowledge/canon/`.
4. Рендерить і експортує монтаж універсально: ffmpeg (headless, всюди), DaVinci Resolve, Premiere/Final Cut через OTIO/FCPXML/EDL, ArtCraft-застосунки через CLI/MCP.

## Не-цілі (YAGNI)

- GUI, вебзастосунок, база даних, хмарна синхронізація.
- Автоматичне встановлення системних залежностей без відома власника.
- Повний паритет ефектів між NLE — межі чесно фіксуються в capability matrix.
- Зберігання медіа в git.

## Ключові рішення

1. **Єдине джерело правди — `timeline.json`** (JSON Schema у `core/schema/`). Час у секундах із дробом; `fps` у meta; timecode генерують конвертери.
2. **Шар адаптерів** з єдиним контрактом: ffmpeg, resolve, otio, artcraft. Кожен адаптер самопровіряється через `probe()`.
3. **Доказова верифікація**: жодного «success» без ffprobe-вимірів (тривалість, fps, стріми, гучність) і витягнутих кадрів.
4. **Канон знань**: `knowledge/inbox/` → процедура дистиляції → `knowledge/canon/`. Свіжіше джерело переважає старіше; конфлікти фіксуються в CHANGELOG; кожне правило має джерело з цитатою.
5. **Bootstrap без тихих інсталяцій**: doctor-звіт із точними командами встановлення; власник вирішує.
6. **Мова документації — українська**; ідентифікатори коду — англійська.
7. **GitHub-репозиторій приватний**: `vaoferi/montage-workflow`.

## Структура репозиторію

```
montage-workflow/
├── AGENTS.md               # вхідна точка для будь-якого агента
├── README.md               # для власника: призначення, ініціалізація
├── bootstrap.sh            # macOS/Linux
├── bootstrap.ps1           # Windows
├── pyproject.toml          # core як Python-пакет
├── core/                   # схема timeline.json, валідація, моделі
│   ├── schema/timeline.schema.json
│   └── montage/            # пакет: validate, doctor, timeline
├── adapters/
│   ├── ffmpeg/             # timeline.json → фільтрграф → рендер + verify
│   ├── resolve/            # Python API: імпорт, таймлайн, маркери, рендер
│   ├── otio/               # експорт FCPXML (FCP) та EDL/XML (Premiere)
│   └── artcraft/           # CLI/MCP: FilmCraft, EffectCraft, AniCraft, SoundCraft, DesignCraft
├── workflow/
│   ├── pipeline.yaml       # етапи: inputs/outputs/tools/gates/evidence
│   └── stages/*.md         # інструкції етапів для агентів (UA)
├── knowledge/
│   ├── inbox/              # ← власник кладе зібраний матеріал
│   ├── canon/              # style/ platform/ audio/ qc/ delivery/ + index.md + CHANGELOG.md
│   └── distill.md          # процедура дистиляції
├── scripts/                # inventory, proxy, preflight (тонкі CLI над core)
├── projects/
│   └── _template/          # brief.md, selects/, audio/, graphics/, timeline.json, decisions.md, qc/
├── tests/
└── docs/specs/             # цей документ
```

Правила гігієни:

- `projects/<slug>/material/`, `proxies/`, `renders/`, `deliverables/` — gitignored; метадані проєкту (brief, timeline, decisions, selects-списки) — у git.
- `machine.yaml` (локальні шляхи, GPU, доступні адаптери) — gitignored.
- Секрети в репо не потрапляють; медіа-посилання в таймлайні відносні до теки проєкту.

## Модель даних `timeline.json`

- `meta`: `project`, `fps`, `resolution {w,h}`, `color_space`, `created`, `platform_targets[]`.
- `tracks[]`: `type` (video/audio/text/overlay), `name`, `items[]`.
- `item`: `id`, `kind` (clip/gap/title/overlay/audio), `source`, `in`, `out`, `effects[]`, `transition_in/out {type, duration}`, `gain_db`, `text{...}`.
- Час — секунди (дробові); кадри рахуються від `fps` meta.
- Валідація: відповідність схемі, існування джерел, консистентність fps/роздільності, відсутність перекриттів на доріжці, сумарна тривалість.

## Контракт адаптера

```
probe(env) -> {available, version, capabilities[], notes[]}
build(timeline, options) -> artifacts     # ffmpeg: команда; resolve: дії API; otio: файл; artcraft: виклики
verify(output) -> measurements            # ffprobe + кадри + loudness
```

- `probe()` визначає доступність на конкретній машині; результат пишеться в `machine.yaml` і capability matrix.
- Capability matrix (`adapters/README.md`) — чесна таблиця підтримки фіч: різка, переходи, оверлеї, титри, багатодоріжкове аудіо, loudnorm, колір.
- Критичні фічі, яких немає в NLE-адаптері, дублюються ffmpeg-рендером.

## Пайплайн (`workflow/pipeline.yaml`)

| # | Етап | Вхід | Вихід | Гейт |
|---|------|------|-------|------|
| 0 | knowledge-distill | `knowledge/inbox/` | оновлений `canon/` + CHANGELOG + звіт | рев'ю власника |
| 1 | brief | запит власника | `brief.md` (платформа, формат, тривалість, дедлайн) | — |
| 2 | ingest-inventory | матеріал | інвентар (ffprobe/ExifTool), проксі, хеші | — |
| 3 | selects | інвентар, канон | шорт-лист, транскрипти (Whisper), теги | — |
| 4 | assembly | selects, канон | `timeline.json` v1 + `decisions.md` | — |
| 5 | rough-cut-gate | рендер ffmpeg | перегляд власником, правки | **людський** |
| 6 | fine-cut | фідбек | `timeline.json` v2 (трими, переходи, ритм) | — |
| 7 | audio | канон audio | мікс, loudnorm за платформою | — |
| 8 | graphics-titles | канон style | титри/графіка (ArtCraft або ffmpeg/ASS) | — |
| 9 | color | канон style | корекція (Resolve; базово — ffmpeg) | — |
| 10 | qc-gate | чекліст qc | виміри + кадри + чекліст | **доказовий** |
| 11 | deliver | канон delivery | матриця експорту, неймінг, архів | — |

Поки канон порожній, діють розумні дефолти; матеріал власника їх заміщує.

## Процедура дистиляції знань

1. Тригер: власник кладе файли/нотатки в `knowledge/inbox/`.
2. Інвентаризація inbox (типи, дати, джерела).
3. Витяг правил і мапінг у категорії: `style/`, `platform/`, `audio/`, `qc/`, `delivery/`.
4. Дедуплікація; конфлікти розв'язуються на користь свіжішого джерела, обидві версії — у CHANGELOG з датами.
5. Кожне правило: джерело (файл + цитата), дата, статус (active/superseded).
6. Оновлення `canon/index.md`; звіт власнику про зміни.

## Bootstrap і перевірка оточення

- `bootstrap.sh` (POSIX) / `bootstrap.ps1` (Windows): ОС, Python ≥ 3.11, ffmpeg/ffprobe, ExifTool, git; опційно Whisper, Resolve, ArtCraft launcher.
- Відсутні залежності → звіт з точними командами встановлення під конкретну ОС; нічого не встановлюється автоматично.
- `machine.yaml` — локальний профіль машини (gitignored).
- `python -m montage doctor` — той самий звіт без побічних ефектів.

## Тестування і CI

- pytest: валідація схеми (валідні/невалідні кейси), побудова ffmpeg-команд (golden-тести), парсинг канону, розв'язання конфліктів.
- Smoke-тест: ffmpeg генерує синтетичні кліпи → `timeline.json` → рендер → ffprobe-перевірка.
- GitHub Actions matrix: `ubuntu-latest`, `macos-latest`, `windows-latest` — pytest + smoke-рендер.

## Ризики й обмеження

- Fidelity OTIO/FCPXML не 100% — фіксується в capability matrix; критичні фічі дублюються ffmpeg-рендером.
- Resolve API доступний лише там, де встановлено Resolve Studio — адаптер опційний.
- ArtCraft-застосунки в активній розробці (FilmCraft in development) — статус перевіряється `probe()` при кожному запуску.
- Крос-платформні шляхи: тільки `pathlib`, жодних хардкодів роздільників.

## Відкриті питання

Немає.
