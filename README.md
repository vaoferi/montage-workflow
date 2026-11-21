# montage-workflow

Універсальний воркфлоу монтажу відео для ШІ-агентів: портативний, кросплатформний, з єдиним каноном знань і скілом-оркестратором.

Приватний репозиторій. Ініціалізується клонуванням на будь-якому ПК (macOS, Linux, Windows); агент читає канон і веде повний маршрут — від сирої теки з матеріалом до переглянутого результату в редакторі.

## Як це працює

1. **Ти кладеш матеріал** — нотатки, референси, приклади стилю, інструкції — у `knowledge/inbox/`.
2. **Агент дистилює** матеріал у канон `knowledge/canon/` (кожне правило з джерелом і датою, історія — в `CHANGELOG.md`).
3. **Для монтажу** агент використовує скіл `skills/montage-director/`: обов'язковий canon-brief → doctor → питання про обсяг → інвентар → транскрипція → маркування повторів/єкань → інтерв'ю → сценарій → монтаж → відкриття в редакторі → QC.
4. **Нічого не лежить без діла**: кожен матеріал стає правилом у каноні; кожен скіл — у маршруті; канон обов'язково читається перед роботою (бриф генерує `scripts/brief.py`).

## Структура

```
knowledge/
├── inbox/          # сирий матеріал власника (недоторканний аудит)
├── canon/          # універсальні правила (style, audio, qc, process, tools)
└── domains/        # доменні інстанси (наприклад, wedding) — не дефолт

skills/montage-director/   # скіл-оркестратор (+ scripts, tests, evals)
workflow/                  # pipeline.yaml і документація етапів (у планах)
docs/specs/                # дизайн-специфікації
projects/                  # робочі теки проєктів (медіа не комітиться)
```

## Швидкий старт

```bash
git clone git@github.com:vaoferi/montage-workflow.git
cd montage-workflow
```

Відкрий теку в агенті (Qoder/Claude Code/Codex/OpenCode) і скажи:
> «Змонтуй відео, матеріал у папці footage»

Агент згенерує canon-brief, перевірить оточення (`doctor`), спитає, який матеріал брати, зробить інвентар і транскрипцію, позначить шлак, поставить питання по суті — і поведе далі за маршрутом.

### Скіл для агента

Джерело правди — `skills/montage-director/`. Для локального використання:

```bash
ln -s "$(pwd)/skills/montage-director" ~/.qoder/skills/montage-director
```

Канон шукається за `MONTAGE_WORKFLOW_ROOT` → предками поточної теки → `knowledge/canon/index.md`.

## Вимоги

- Python 3.9+ (скрипти скіла — stdlib)
- ffmpeg / ffprobe
- безкоштовний транскрибатор: `pip install faster-whisper`
- редактор за бажанням: DaVinci Resolve (безкоштовний), Premiere, Final Cut, FilmCraft

`doctor` покаже, що встановлено, і дасть точні команди для відсутнього. Системні пакети — лише з дозволу власника.

## Канон

Універсальні правила живуть у `knowledge/canon/`; доменні конкретизації — окремо в `knowledge/domains/` і ніколи не замінюють канон.

- `style/` — монтажна граматика, метод аналізу, контрольована динаміка, композиція кадру
- `audio/` — пріоритет звуку, пайплайн відновлення
- `qc/` — протокол перегляду, фінальні заборони (обрізані думки/голови/кінцівки, шлак)
- `process/` — дисципліна агента: evidence-before-Done, test-before-batch, оригінали незмінні, provenance, людські гейти
- `tools/` — довідки про інструменти й реєстр зовнішніх скілів з політикою автооновлення перед застосуванням

## Перевірка скіла (NVIDIA SkillEvaluator)

```bash
uv run --python 3.12 --with pytest pytest skills/montage-director/scripts/tests -q

# Tier 1 (статичні перевірки + сканери)
uv tool install --python 3.12 "git+https://github.com/NVIDIA/SkillSpector.git@v2.13.4"
uv run --python 3.12 --with skillevaluator skillevaluator validate skills/montage-director --tiers 1
```

Поради для повної перевірки з OpenRouter (ключ — локально, ніколи в git):

```bash
export NO_PROXY='*' no_proxy='*'
export SKILL_EVAL_LLM_PROVIDER=openai-compatible \
       SKILL_EVAL_LLM_API_KEY=$OPENROUTER_API_KEY \
       SKILL_EVAL_LLM_BASE_URL=https://openrouter.ai/api/v1 \
       SKILL_EVAL_LLM_MODEL=nvidia/nemotron-3.5-lightning:free \
       SKILL_EVAL_EMBEDDING_PROVIDER=openai-compatible \
       SKILL_EVAL_EMBEDDING_MODEL="nvidia/nemotron-3.5-embed-8b:free"
# Tier 2 (дедуплікація); Tier 3 — з --env-mode local, -a codex, --max-cost-usd 1 --price-file
```

## Правила репозиторію

- Оригінали медіа незмінні; медіа, проксі й рендери ніколи не комітяться.
- `Done` = перевірений результат, а не успішний exit code.
- Зовнішні скіли — залежності: автооновлення з офіційних репо перед застосуванням, фіксація commit SHA.
- Секрети — лише локально (`.secrets/`, gitignored).
