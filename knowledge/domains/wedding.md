# Доменний інстанс: весільний фільм (wedding highlight)

Джерело: матеріал №1 (`knowledge/inbox/2026-09-18-wedding-editorial-advisory.md`), отримано 2026-11-21. Статус: active.

**Це не дефолт канону.** Універсальні правила — у `knowledge/canon/`; цей файл лише конкретизує їх для одного домену. Майбутні домени додаються поруч як окремі файли.

## Ідентичність

Мета — не показати все весілля, а найкращу версію того, яким день запам'ятається людям. Монтаж має виглядати так, ніби кожен кадр обрано навмисно.

## Подієва таксономія

establishing/location → bride preparation → groom preparation → family preparation → arrival → ceremony → entrance → pastor/officiant → vows → rings → kiss → prayer → congratulations → couple portrait session → family → reception → speeches → first dance → party → quiet ending/departure.

Фінальний монтаж не зобов'язаний іти суворо хронологічно, якщо емоційно сильніша структура працює краще.

## Ролі людей

Наречена, наречений, пастор/ведучий, батьки, свідки, близька родина, інші постійні важливі люди.

## Ключові джерела історії

Vows, слова пастора/ведучого, промови, природний діалог батьків і наречених, сміх і реакції. Найсильніші sound bites стають основою narrative spine.

## Мапінг етапів матеріалу на пайплайн

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
