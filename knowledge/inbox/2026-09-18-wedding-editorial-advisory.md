Так. Я б тут **не давав агенту команду “змонтуй весілля красиво”** — це майже гарантований шлях до другої серії “Туфлі: режисерська версія, 4 хвилини” 😄. Йому треба дати **редакторську систему прийняття рішень**.

Я перевірив актуальні матеріали. Станом на **18 вересня 2026 року актуальна лінійка — DaVinci Resolve 21, на сайті Blackmagic уже описана 21.1**. І для твоєї задачі це суттєво краще: IntelliSearch шукає об'єкти, людей, сцени, обличчя і фрази в транскрипції; є стабілізація, Shot Match, Voice Isolation, AI UltraSharpen і Motion Deblur. [Blackmagic Design](https://www.blackmagicdesign.com/ua/products/davinciresolve/whatsnew?utm_source=chatgpt.com)

## Спочатку — що в твоєму розумінні вже правильне

Ти дуже правильно відчув **дві проблеми**.

Перша: кадр не повинен залишатися тільки тому, що оператор його зняв. У сучасному wedding highlight монтажі критерій приблизно такий: **кадр живе доти, доки він дає нову інформацію, емоцію або красу. Коли перестав — різати.** Саме тому три секунди нерухомих туфель можуть бути нестерпно довгими, а чотири секунди реакції батька на наречену — навпаки короткими. Сучасні рекомендації з wedding pacing теж прямо радять змінювати тривалість кадрів відповідно до емоційної фази, а не робити все однаковим. [LoveStoryEditing.com](https://lovestoryediting.com/wedding-video-editing-techniques/pacing-in-wedding-video-editing-the-complete-guide/?utm_source=chatgpt.com)

Друга: **повтори однакової інформації треба безжально прибирати**. Туфлі → через секунду ті самі туфлі → ще один майже такий самий ракурс — це не “покриття”, якщо другий кадр нічого не додає. У професійній спільноті wedding-редакторів одна з найтиповіших рекомендацій — спочатку зробити жорсткий selects/culling усього матеріалу, а вже потім монтувати, саме щоб не набивати timeline повторюваним B-roll. [Reddit](https://www.reddit.com/r/videography/comments/17j2y5j?utm_source=chatgpt.com)

### А от щодо руху камери — поправка

Не існує правила:

> один кліп = тільки один напрямок руху.

Може бути push-in → зупинка → pan, якщо це **мотивовано подією**. Наприклад камера наближається до нареченої, вона обертається до матері, камера слідує за нею.

Поганий варіант:

камера вправо → оператор передумав → назад → трохи вверх → шукає композицію → вниз → знову вправо.

Це не кінематографічний рух. Це **пошук кадру оператором**, який просто потрапив у запис.

Nikon у своїх актуальних рекомендаціях теж підкреслює: рух повинен направляти увагу, а постійне панорамування і різні хаотичні напрямки ускладнюють монтаж і виглядають рвано. [nikon.co.uk](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/get-to-grips-with-pan-and-tilt?utm_source=chatgpt.com)

Тому для твого матеріалу правило агенту я б сформулював жорсткіше:

**залишай завершений намір оператора, вирізай процес пошуку кадру.**

---

# Як AI має аналізувати весілля

Ось тут, думаю, найбільший апгрейд порівняно з твоїми попередніми спробами.

Не треба змушувати агента читати, умовно, **300 000 кадрів як 300 000 незалежних фотографій**. Він отримає цифровий Альцгеймер раніше, ніж дійде до церемонії.

Йому потрібен **ієрархічний аналіз**:

- [ ] Спочатку проіндексувати **всі файли, час, камеру, fps, resolution, audio tracks**.
- [ ] Зробити **повну транскрипцію всього звуку** і визначити, де реально говорять люди.
- [ ] Проаналізувати обличчя й розпізнати мінімум: наречена, наречений, пастор/ведучий, батьки, ключові родичі.
- [ ] Розділити день на події: establishing → bride prep → groom prep → arrival → ceremony → vows → rings → kiss → congratulations → portraits → reception → speeches → first dance → party → ending.
- [ ] Усередині довгих кліпів зробити грубий visual scan, наприклад кожні 0,5–1 секунду.
- [ ] Якщо виявлено зміну дії, сильну емоцію, мову, сміх, обійми, сльози, кільця, поцілунок тощо — перейти до **щільного аналізу цього відрізка**.
- [ ] Позначити технічну якість: focus, motion blur, shake, exposure, blown highlights, noise, obstruction, backs of heads, погана композиція.
- [ ] Знайти майже дублікати і об'єднати їх у групи: `shoes_01`, `shoes_02`, `shoes_03`; `bride_makeup_01…`.
- [ ] Усередині групи залишити **найсильніший варіант**, а не всі.
- [ ] Окремо створити `MUST KEEP`, `GOOD`, `UTILITY B-ROLL`, `RESCUE`, `REJECT`.
- [ ] Спочатку побудувати **історію зі змістовного аудіо**: vows, speeches, молитва/слова пастора, природні емоційні фрази.
- [ ] Потім накривати цю історію B-roll, а не навпаки.
- [ ] Перед фіналом повністю передивитися timeline **в реальному часі**, а не оцінювати тільки окремі кадри.

І це добре збігається з можливостями Resolve 21: IntelliSearch уміє шукати окремо за **visual content, transcript і metadata**, показувати обличчя та навіть повертати релевантний сегмент усередині довгого кліпу. [Blackmagic Design Documents](https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_21_New_Features_Guide.pdf?_v=1776322810000\&utm_source=chatgpt.com)

## Формула оцінки кадру

Я б не наказував агенту просто вибирати “найкрасивіший”.

Нехай він для кожного кандидата оцінює:

**Story → Emotion → Human significance → Technical quality → Composition → Novelty → Continuity.**

Саме в такому приблизно порядку.

Тобто чудово зняті квіти **не повинні перемогти** трохи shaky кадр, де тато вперше побачив доньку у весільній сукні.

Але якщо є три однакових кадри цієї реакції — вибираємо технічно найкращий.

---

# Що робити з поганою зйомкою

Тут Resolve Studio реально може частину лайна перетворити хоча б на компост 🌚.

**Shaky кадр:** спочатку trim поганого початку/кінця → потім Stabilization. Resolve дозволяє контролювати smoothing, strength, crop та навіть Camera Lock. [Blackmagic Design](https://www.blackmagicdesign.com/products/davinciresolve/edit?utm_source=chatgpt.com)

**Камера елозить туди-сюди:** часто найкращий ремонт — не стабілізація всього кліпу, а **вирізати 1–2 чистих фрагменти між змінами напрямку**.

**Трохи промахнулися фокусом:** Resolve 21 Studio отримав AI UltraSharpen саме для незначно soft/out-of-focus матеріалу. Це rescue, не воскресіння трупа. [Blackmagic Design Documents](https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_21_New_Features_Guide.pdf?utm_source=chatgpt.com)

**Motion blur:** у 21 є AI Motion Deblur. Особливо корисний перед slow motion/freeze frame. [Blackmagic Design](https://www.blackmagicdesign.com/ca/products/davinciresolve/whatsnew?utm_source=chatgpt.com)

**Різний колір камер:** спочатку технічна нормалізація → WB/exposure → skin tones → shot matching → уже потім creative look. Resolve вміє Shot Match за кольором, контрастом і яскравістю. [Blackmagic Design](https://www.blackmagicdesign.com/ca/products/davinciresolve/color?utm_source=chatgpt.com)

**Поганий звук:** vows/speeches треба рятувати раніше за “красивий LUT”. Fairlight має cleanup, Voice Isolation та automatic ducking музики під діалог. [Blackmagic Design](https://www.blackmagicdesign.com/products/davinciresolve/fairlight?utm_source=chatgpt.com)

І я тут повністю погоджуся з сучасною практикою wedding editing: **слова й живий звук часто несуть історію сильніше за картинки**. Vows і speeches зараз фактично стали одним із основних narrative tools wedding film. [Bride&Groom.video](https://bridengroom.video/blog/vows-speeches-wedding-video/?utm_source=chatgpt.com)

---

# Щодо напрямку між кадрами

Тут уже правила реальніші.

Якщо людина йде **зліва направо**, у наступному кадрі без причини не варто раптом змушувати її рухатися **справа наліво**. Те саме стосується pan, поглядів і просторової орієнтації.

Це screen direction / 180-degree continuity. Зламати її можна, але краще через **wide shot, neutral shot, cutaway або видимий рух, що пояснює зміну осі**. [adobe.com](https://www.adobe.com/uk/creativecloud/video/discover/what-is-the-180-degree-rule.html?utm_source=chatgpt.com)

Тому агенту треба аналізувати не тільки сам кадр, а ще:

`previous shot → candidate shot → following shot`.

Це дуже важливо.

Бо кадр може бути прекрасним **окремо**, але жахливим **після попереднього**.

---

# Про тривалість кадрів

Не вводив би правило “всі B-roll 1,5 секунди”.

Але агенту потрібні орієнтири.

Для швидкої підготовки: маленькі деталі типу туфель, парфумів, запонок, кілець часто можуть працювати **~0,7–2 с**.

Для красивого establishing/detail кадру: приблизно **1,5–3 с**.

Для людської реакції: **2–5+ с**, якщо емоція продовжує розвиватися.

Для vows, prayer, speeches: кадр може жити значно довше.

Для dance/reception montage: часто швидше, але прив'язано до музичної фрази та дії.

І ще краще правило:

**не “скільки секунд?”, а “коли глядач уже все зрозумів?”**

Дослідження сучасного B-roll монтажу дають широкий орієнтир близько 2–5 секунд, але wedding/highlight монтаж часто буде агресивнішим на деталях. [Video Editing: Workflow, Codecs & Fixes](https://www.editorcuts.com/blog/what-is-b-roll-how-to-use?utm_source=chatgpt.com)

---

# Готовий master prompt для агента

Це вже можеш давати OpenCode/Codex/іншому агенту як **редакторську конституцію**, а не разове завдання.

Ти працюєш як senior wedding film editor і монтажний режисер у DaVinci Resolve Studio.

Твоя задача не полягає в тому, щоб використати якомога більше відзнятого матеріалу. Твоя задача — знайти всередині погано або нерівномірно відзнятого весілля найсильнішу людську історію та змонтувати її так, щоб результат виглядав навмисно знятим і професійно змонтованим.

ГОЛОВНИЙ ПРИНЦИП

Кожен кадр повинен виправдовувати своє перебування у фінальному монтажі хоча б одним із факторів:

1. просуває історію;
2. показує важливу подію;
3. передає сильну людську емоцію;
4. дає нову інформацію;
5. створює потрібний ритм або атмосферу;
6. необхідний як монтажне покриття.

Сам факт існування кадру не є причиною його використовувати.

ПРІОРИТЕТИ

Story > emotion > people > technical quality > beauty > quantity of footage.

Трохи технічно слабший, але унікальний емоційний момент важливіший за ідеально знятий декоративний кадр.

Якщо одна й та сама інформація повторюється декілька разів, вибери найкращий варіант і видали дублікати.

Не використовуй кадр повторно без чіткої драматургічної причини.

ЕТАП 1. ІНВЕНТАРИЗАЦІЯ

Перед монтажем проаналізуй весь матеріал.

Для кожного media file визнач:

- camera/source;
- resolution;
- fps;
- duration;
- audio presence;
- people present;
- approximate event;
- visual quality;
- camera movement;
- useful dialogue;
- emotional events.

Транскрибуй весь доступний звук.

Визнач основних людей:

- bride;
- groom;
- parents;
- pastor/officiant;
- witnesses;
- close family;
- other recurring important people.

ЕТАП 2. ПОДІЇ

Згрупуй матеріал приблизно за такими сценами, якщо вони присутні:

establishing / location
bride preparation
groom preparation
family preparation
arrival
ceremony
entrance
pastor/officiant
vows
rings
kiss
prayer
congratulations
couple portrait session
family
reception
speeches
first dance
party
quiet ending / departure.

Не змушуй фінальний монтаж суворо йти хронологічно, якщо емоційно сильніша структура працює краще.

ЕТАП 3. БАГАТОПРОХІДНИЙ АНАЛІЗ

Не аналізуй кожен frame усього матеріалу з однаковою деталізацією.

Pass A:
зроби швидкий scan всього відео, використовуючи scene changes, thumbnails/frame sampling, audio waveform, transcription і semantic analysis.

Pass B:
знайди потенційно значущі ділянки:

- speech;
- vows;
- laughter;
- crying;
- hugs;
- kisses;
- eye contact;
- prayer;
- rings;
- entrance;
- first look;
- applause;
- reactions;
- dancing;
- interactions between bride/groom and family.

Pass C:
для цих ділянок зроби значно щільніший frame-level аналіз і знайди найкращі in/out points.

ЕТАП 4. КЛАСИФІКАЦІЯ

Познач фрагменти:

MUST KEEP
Унікальний ключовий момент весілля.

STRONG
Сильна емоція, дія або красивий корисний кадр.

UTILITY
Корисний B-roll для покриття монтажу.

RESCUE
Зміст важливий, але відео має технічні проблеми, які можливо виправити.

REJECT
Немає значущої дії або кадр технічно/композиційно неприйнятний.

До REJECT зазвичай належать:

- люди просто чекають без значущої взаємодії;
- довгі фрагменти, де нічого не відбувається;
- оператор шукає композицію;
- випадкові спини людей;
- напівпорожні кадри без композиційної мети;
- невдалий focus hunting;
- камера опускається або піднімається без змісту;
- початок/кінець запису до або після корисної дії;
- повтори вже показаних деталей;
- слабші дублікати тієї самої події.

ЕТАП 5. ДУБЛІКАТИ

Кластеризуй візуально та семантично схожі кадри.

Наприклад:

shoes
rings
dress
flowers
groom dressing
bride makeup
venue exterior
couple walking
guests waiting.

Не використовуй декілька майже однакових кадрів поспіль.

Якщо один detail shot вже повністю передав інформацію, наступний схожий кадр повинен показати новий ракурс, дію або емоцію. Інакше видали його.

ЕТАП 6. РУХ КАМЕРИ

Відрізняй intentional camera movement від operator searching.

Intentional movement:
smooth pan;
tilt;
push-in;
pull-out;
tracking;
reveal;
movement following subject.

Operator searching:
безпричинний pan right → left;
reframing;
camera hunting;
start-stop-start movement;
виправлення горизонту;
випадкове наближення;
рух до об'єкта і від нього без змістовної причини.

Зберігай завершений навмисний рух.

Вирізай процес пошуку композиції.

Якщо корисна частина знаходиться посеред поганого довгого shot, використовуй тільки чистий фрагмент.

Не застосовуй stabilization автоматично до всього матеріалу. Використовуй її тільки там, де вона покращує кадр без неприродного warp/crop.

ЕТАП 7. CONTINUITY

Перед кожною склейкою оцінюй не лише обидва кадри окремо, а пару:

previous shot → next shot.

Перевір:

screen direction;
subject movement;
eye line;
camera movement direction;
subject position in frame;
brightness;
color;
scale;
visual weight.

Уникай випадкової зміни screen direction.

Якщо зміна напрямку необхідна, використовуй neutral shot, wide establishing shot, reaction shot або інший visual reset.

Cut on action whenever appropriate.

Не роби hard cut між двома майже однаковими планами одного об'єкта, якщо різниця ракурсу/крупності надто мала і виникає випадковий jump cut.

ЕТАП 8. РИТМ

Не використовуй однакову тривалість для всіх кадрів.

Тривалість визначає зміст кадру.

Деталі під час енергійного montage повинні бути короткими.

Не змушуй глядача декілька секунд розглядати туфлі, квіти, запонки або декор, якщо після першої секунди він уже отримав всю інформацію.

Людські реакції можуть тривати значно довше, якщо емоція розвивається.

Під час vows, speeches, prayer і важливих діалогів не жертвуй змістом заради швидких cuts.

Правило:

Hold the shot while it is still giving the viewer new information, emotion or beauty.
Cut when it stops.

ЕТАП 9. STORY FIRST

Перед основним visual edit створи narrative spine.

Прослухай:

vows;
pastor/officiant;
speeches;
natural dialogue;
parents;
bride/groom;
laughter and reactions.

Виділи найсильніші sound bites.

Будуй історію навколо людей і їхніх слів, а не навколо декоративного B-roll.

B-roll повинен підтримувати історію, приховувати монтажні переходи і показувати те, про що йдеться.

Не використовуй B-roll лише тому, що він красивий.

ЕТАП 10. AUDIO

Пріоритет:

dialogue / vows / speeches
→ meaningful natural sound
→ ambience
→ music.

Музика не повинна маскувати мову.

Використовуй cleanup / voice isolation лише настільки, наскільки це не створює неприродного голосу.

Зберігай природні звуки там, де вони додають присутності:

laughter;
applause;
room tone;
dress movement;
doors;
steps;
rings;
kiss reaction;
crowd reaction.

ЕТАП 11. COLOR

Спочатку забезпеч технічну послідовність кадрів:

correct input color space;
white balance;
exposure;
contrast;
skin tone;
camera matching.

Після цього формуй creative look.

Усі кадри однієї сцени повинні виглядати так, ніби вони існують в одному просторі.

Не копіюй один grade сліпо на все весілля.

Особливо контролюй skin tone.

ЕТАП 12. SALVAGE

Якщо важливий кадр має дефект, спробуй врятувати його.

Можливі інструменти:

crop / reframe;
stabilization;
noise reduction;
UltraSharpen для невеликого промаху фокусу;
Motion Deblur;
speed adjustment;
shorter in/out;
B-roll coverage;
color correction.

Не намагайся врятувати технічно поганий кадр тільки тому, що він існує.

Якщо інформацію або емоцію можна передати кращим кадром, використовуй кращий кадр.

ЕТАП 13. ФІНАЛЬНИЙ QC

Після rough cut переглянь відео повністю від початку до кінця в реальному часі.

Під час перегляду не редагуй.

Створи список моментів, де:

- стало нудно;
- повторюється інформація;
- незрозуміло, куди дивитися;
- рух різко змінив напрямок;
- занадто довгий detail shot;
- музика перекриває слова;
- зламався emotional build;
- колір стрибнув;
- кадр технічно відволікає;
- одна людина або подія отримала непропорційно багато screen time.

Після перегляду виправ ці місця.

Потім зроби другий QC pass.

ГОЛОВНЕ ПРАВИЛО

Не показуй усе весілля.

Покажи найкращу версію того, яким цей день запам'ятається людям.

Монтаж повинен виглядати так, ніби кожен кадр обрано навмисно.

Я б саме **цей текст зберіг як постійну інструкцію/skill**, а конкретне весілля вже запускав другим промптом.

## Що я б ще додав агенту технічно

Якщо у тебе агент реально може писати Python і керувати Resolve, це вже стає серйозно цікаво. Resolve 21.1 має scripting API для Python/Lua, а актуальна API поверхня дозволяє працювати з Media Pool, створювати timelines, задавати in/out та додавати markers; у Studio через API доступні також AI-операції на кшталт IntelliSearch analysis і transcription. [wheheohu.github.io](https://wheheohu.github.io/bmd_doc/ResolveAPI/intro?utm_source=chatgpt.com)

Тобто я б **не одразу дозволяв AI фізично фіналізувати монтаж**. Розумніша схема:

**AI analysis → markers + metadata + selects timeline → AI rough cut → human review → AI revision → color/audio → final QC.**

Так значно безпечніше.

Наприклад агент може ставити маркери:

`GREEN = MUST KEEP`  
`BLUE = good B-roll`  
`PURPLE = emotional`  
`YELLOW = dialogue`  
`ORANGE = rescue needed`  
`RED = reject/problem`

А вже потім складати з `GREEN + PURPLE + YELLOW` narrative skeleton.

Це буде **набагато розумніше**, ніж “проаналізував папку → створив ролик”.

### І головна зміна, яку я б зробив порівняно з твоїми попередніми спробами

Не починай із музики й красивих перебивок.

Спочатку:

**хто ці люди → що відбулося → де найсильніші слова → де найсильніші реакції → яка емоційна дуга → і лише потім красиві картинки.**

У wedding editing спільноті рівно це регулярно повторюється: спочатку selects і narrative/audio structure, потім visuals, потім music/refinement/color. [Reddit](https://www.reddit.com/r/videography/comments/17j2y5j?utm_source=chatgpt.com)

Тоді туфлі перестають бути головними героями весілля. І це вже прогрес. 😄

Якщо захочеш довести це до нормальної **четвертої спроби**, наступним кроком я б уже зробив тобі **технічний prompt для OpenCode/Codex**, де агент не просто знає правила, а сам: аналізує файли → запускає Resolve 21 IntelliSearch/transcription → розставляє markers → створює `SELECTS` timeline → `STORY AUDIO` timeline → `ROUGH CUT v1`. Це якраз той рівень автоматизації, де AI починає приносити користь, а не генерувати випадковий “весільний кліп”.