# Зовнішні скіли: реєстр і політика

Джерело: матеріал №6 (`knowledge/inbox/2026-11-21-external-skills-advisory.md`), отримано 2026-11-21. Статус: active.
Застосовність: будь-який агент, будь-яка машина.

Зовнішні Agent Skills — це **залежності**, а не канон. Рішення про сюжет, кадр і звук ухвалює канон (`knowledge/canon/`), скіли лише виконують.

## Політика (обов'язкова)

1. **Автооновлення перед застосуванням.** Перед використанням у роботі — sync кожного скіла з його офіційного репо до актуального стану. Зафіксувати використаний commit SHA (provenance, `process/agent-discipline.md`). Ніколи не запускати застарілий локальний стан.
2. **Огляд змін перед запуском.** Скіли виконують код: після sync переглянути дифф/реліз-ноти; неперевірене оновлення не запускати негайно в робочому проєкті.
3. **Мінімальний набір.** Не встановлювати все підряд — частина скілів перекривається. Ставити лише те, що закриває конкретну потребу (native-before-dependency вже діє).
4. **Перший запуск — smoke test.** Новий або оновлений скіл вперше запускається на одному реальному відео/фрагменті з переглядом результату (test before batch).
5. **Перегляд зі звуком.** Змонтований ролик обов'язково дивитися зі звуком: AI часто бездоганно вирізає паузу разом із половиною сенсу.
6. **Офіційність джерел.** Оновлення лише з офіційних репо. Форки та сумнівні джерела — окреме рішення власника.

## Реєстр (перевірено 2026-11-21)

Ланцюг продакшену: сюжет → сценарій → розкадрування → картинки → B-roll → монтаж → анімації → субтитри → QC.

| Репо | Сильна сторона | Стан перевірки | Роль у воркфлоу |
|------|----------------|----------------|------------------|
| `nateherkai/herk-edit-kit` | 15 скілів, 406 motion-карток, transcript-driven cuts, B-roll, субтитри; потребує Node.js, FFmpeg, Chromium, HyperFrames; платні API необов'язкові | public, ~3k★, оновлений 2026-11-21 | №1 для готових роликів; встановлювати цілий репо за README (скрипти, шаблони, локальний рушій) |
| `novincode/creator-skills` | story-craft, hook-craft, script-writing, storyboarding, visual-prompting, motion-design, sound-design; частина компонентів alpha/beta | public, оновлений 2026-11-17 | №1 для творчої частини |
| `vyralcontent/content-skills` | хуки, сценарії, Shorts/Reels/TikTok, утримання уваги | public, ~270★ | вірусний формат |
| `social-media-skills/video-editing-skill` | розмовні відео: паузи, дублі, субтитри, punch-ins, clean audio | public | talking-head монтаж |
| `kajisho5/ffmpeg-skill` | 42 інструменти, machine-readable contract + MCP server, без хмари й API-ключів | public, ~9k★ | технічна основа |
| `remotion-dev/skills` | анімація тексту/графіки/переходів кодом; офіційні скіли | public, ~8k★ | візуальне оформлення |
| `Benitoow/cinema-skills` | монтажний план, структура сцен, колір, ритм | public, малий repo | режисура (опційно) |
| `leynos/visual-storytelling-skills` | планування кадрів, візуальна послідовність, сталість персонажів | public, малий repo | AI-сцени (опційно) |
| `mattpocock/skills` | інженерні скіли для агентів, «Straight from my .agents directory» | public, ~330k★ | інженерна дисципліна; доповнює `process/` |

## Додаткові адаптери web showcase (2026-11-24)
Окремий домен: `knowledge/domains/web-project-showcase.md`. Вибір, реальні обмеження та candidate SHA: `web-showcase-tools.md`. Stageshow, demo-video-skills, chrome-capture, Subtle — optional entries у registry, синхронізувати лише через `--only` за потреби, не встановлювати глобально.

## Рекомендований стартовий стек

Creator Skills (story-craft, storyboarding) + Vyral (viral-hooks) + video-editing-skill + ffmpeg-skill + remotion-dev/skills + mattpocock/skills.

Перший реальний тест: Herk Edit Kit + Creator Skills + ffmpeg-skill — перевірити якість сюжету, доречність картинок, коректність субтитрів, відсутність обірваних думок.

## Синхронізація (автооновлення)

Усі репо з реєстру (`skills/external/registry.json`) синхронізуються в локальний пул `~/.qoder/skill-pool`:

```bash
python3 scripts/skills_sync.py                  # усі репо: clone або shallow-оновлення
python3 scripts/skills_sync.py --only owner/name  # точкове оновлення
```

- Кожен синк записує точний commit SHA у `skills/external/lock.json` (provenance; файл комітиться).
- Перед використанням скіла в роботі — обов'язковий синк (політика вище).
- До агента підключаються **точково** потрібні скіли (симлінк у `~/.qoder/skills/`), а не всі одразу: 50+ описів у контексті шкодять якості.

## Встановлення (приклад для OpenCode)

```
npx skills add novincode/creator-skills --skill story-craft -a opencode
npx skills add novincode/creator-skills --skill storyboarding -a opencode
npx skills add vyralcontent/content-skills --skill viral-hooks -a opencode
npx skills add social-media-skills/video-editing-skill -a opencode
npx skills add kajisho5/ffmpeg-skill -a opencode
npx skills add remotion-dev/skills -a opencode
```

Herk Edit Kit — цілий репозиторій за README.

## Межі

- Для генерації нових зображень і кадрів скіли лише готують завдання та промпти; потрібен окремий генератор (Magnific, Descript — окремі інтеграції, не локальні скіли).
- Оцінка можливостей — за документацією джерел; незалежного тесту на реальному відео ще не було (станом на 2026-11-21).
- Скіл не замінює канон: творчі й технічні рішення — з `knowledge/canon/`, доменні — з `knowledge/domains/`.
