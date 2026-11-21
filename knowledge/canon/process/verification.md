# Верифікація: Done = evidence

Джерело: матеріал №3 (`knowledge/inbox/2026-11-21-governance-principles-advisory.md`), отримано 2026-11-21. Статус: active.
Застосовність: будь-який монтаж і будь-яке processing.

## Принцип

`Done` означає перевірений результат. Успішне виконання CLI-команди, скрипта, Resolve API call або inference моделі **не є доказом** якісного результату.

Не повідомляти «успішно покращено», якщо перевірено лише exit code.

## Рівень доказів відповідає ризику

| Дія | Обов'язкова перевірка |
|-----|------------------------|
| audio restoration | прослухати A/B; intelligibility; артефакти |
| video denoise | 100% crop + motion review |
| stabilization | весь processed shot на warp/crop |
| color | scopes + skin + сусідні shots |
| rough cut | перегляд sequence у реальному часі |
| final | повний QC render |

## Test before batch

Ніколи не застосовувати дорогий, destructive-looking або AI-heavy processing до всього матеріалу лише тому, що він спрацював на одному shot.

Перед batch:

1. визначити problem class;
2. вибрати representative difficult sample;
3. створити processed candidate;
4. зробити A/B comparison;
5. перевірити артефакти;
6. лише після цього масштабувати на відповідну групу clips.

Не робити global replacement без reviewed target list.

## Media-TDD

Аналог TDD для media-processing:

problem sample → baseline evidence → minimal candidate processing → A/B verification → apply to target class → regression/QC check.

- Не видаляти baseline/original лише тому, що новий processed result виглядає кращим.
- Не ослаблювати QC-критерій, щоб processing міг вважатися «успішним».

## Об'єктивне vs суб'єктивне

Об'єктивні інваріанти краще перевіряти машиною, ніж багаторазово писати в Markdown. Кандидати для автоматичних перевірок (`scripts/project_check.py`-клас):

- originals не лежать у generated/output теках;
- немає overwrite source paths;
- derived audio має provenance;
- transcript існує для analyzed speech;
- output не має missing media;
- очікувані FPS / роздільність таймлайна правильні;
- final audio не clipping;
- generated assets не втратили source mapping.

Суб'єктивне судження — «кадр красивий», «ритм достатньо емоційний», «цей push-in доречний» — **не** перетворювати на крихкі машинні тести.

Деталі канону про монтажні правила — `style/`, але enforcement — лише для об'єктивних інваріантів.

## Звітність агента

Звіт про завершення роботи має містити:

- що створено;
- що мігровано;
- які правила були дублями;
- які конфлікти знайдено;
- що залишилось unresolved;
- які перевірки реально виконані.

Не називати setup завершеним лише тому, що файли створені. Перевірка: новий агент, прочитавши AGENTS.md → project-рівень → routed docs, отримує достатній контекст для продовження роботи без повторного пояснення всього проєкту.
