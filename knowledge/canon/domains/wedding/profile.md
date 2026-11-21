# Домен: весільний фільм (wedding highlight)

Джерело: матеріал №1 (`knowledge/inbox/2026-09-18-wedding-editorial-advisory.md`), отримано 2026-11-21. Статус: active.

## Ідентичність

Мета — не показати все весілля, а найкращу версію того, яким день запам'ятається людям. Монтаж має виглядати так, ніби кожен кадр обрано навмисно.

## Багатопрохідний аналіз (Pass A/B/C)

- **Pass A** — швидкий скан усього матеріалу: scene changes, thumbnails/frame sampling (грубо кожні 0.5–1 с усередині довгих кліпів), audio waveform, транскрипція, семантичний аналіз. Не аналізувати кожен кадр усього матеріалу з однаковою деталізацією.
- **Pass B** — знайти потенційно значущі ділянки: мова, vows, сміх, сльози, обійми, поцілунки, eye contact, молитва, кільця, вхід, first look, аплодисменти, реакції, танці, взаємодія наречених з родиною.
- **Pass C** — щільний frame-level аналіз цих ділянок: найкращі in/out points.

## Подієва таксономія (орієнтовна)

establishing/location → bride preparation → groom preparation → family preparation → arrival → ceremony → entrance → pastor/officiant → vows → rings → kiss → prayer → congratulations → couple portrait session → family → reception → speeches → first dance → party → quiet ending/departure.

Фінальний монтаж не зобов'язаний іти суворо хронологічно, якщо емоційно сильніша структура працює краще.

## Люди

Ідентифікувати мінімум: наречена, наречений, пастор/ведучий, батьки, свідки, близька родина, інші постійні важливі люди.

## Класифікація фрагментів

- **MUST KEEP** — унікальний ключовий момент весілля.
- **STRONG** — сильна емоція, дія або красивий корисний кадр.
- **UTILITY** — корисний B-roll для покриття монтажу.
- **RESCUE** — зміст важливий, але є технічні проблеми, які можливо виправити.
- **REJECT** — немає значущої дії або кадр технічно/композиційно неприйнятний.

Типові REJECT-ознаки:

- люди просто чекають без значущої взаємодії;
- довгі фрагменти, де нічого не відбувається;
- оператор шукає композицію;
- випадкові спини людей;
- напівпорожні кадри без композиційної мети;
- невдалий focus hunting;
- камера опускається/піднімається без змісту;
- початок/кінець запису до або після корисної дії;
- повтори вже показаних деталей;
- слабші дублікати тієї самої події.

## Дублікати

Кластеризувати візуально й семантично схожі кадри: shoes, rings, dress, flowers, groom dressing, bride makeup, venue exterior, couple walking, guests waiting.

Усередині кластера лишається найсильніший варіант. Кілька майже однакових кадрів поспіль — заборонено.

## Narrative spine

Спочатку прослухати: vows, pastor/officiant, speeches, природний діалог, батьків, наречених, сміх і реакції. Виділити найсильніші sound bites.

Історія будується навколо людей і їхніх слів, а не навколо декоративного B-roll.

## Маркери в NLE (конвенція)

| Колір | Значення |
|-------|----------|
| GREEN | MUST KEEP |
| BLUE | good B-roll |
| PURPLE | emotional |
| YELLOW | dialogue |
| ORANGE | rescue needed |
| RED | reject/problem |

Narrative skeleton складається з GREEN + PURPLE + YELLOW.

## Безпека автоматизації

Схема: AI analysis → markers + metadata + SELECTS timeline → AI rough cut → людське рев'ю → AI revision → color/audio → final QC.

Агент не фіналізує монтаж без людського гейта.

## Мапінг на пайплайн

| Етап матеріалу | Стадія `workflow/pipeline.yaml` |
|----------------|----------------------------------|
| ЕТАП 1 інвентаризація | 2 ingest-inventory |
| ЕТАП 2 події | 2 ingest-inventory → 3 selects |
| ЕТАП 3 аналіз A/B/C | 3 selects |
| ЕТАП 4 класифікація | 3 selects |
| ЕТАП 5 дублікати | 3 selects |
| ЕТАП 6 рух камери | 3 selects → 6 fine-cut |
| ЕТАП 7 continuity | 4 assembly → 6 fine-cut |
| ЕТАП 8 ритм | 6 fine-cut |
| ЕТАП 9 story first | 4 assembly |
| ЕТАП 10 audio | 7 audio |
| ЕТАП 11 color | 9 color |
| ЕТАП 12 salvage | 6 fine-cut |
| ЕТАП 13 final QC | 10 qc-gate |
