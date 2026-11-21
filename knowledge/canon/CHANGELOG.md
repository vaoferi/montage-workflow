# CHANGELOG канону

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
