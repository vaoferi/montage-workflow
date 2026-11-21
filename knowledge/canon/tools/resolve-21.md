# Інструменти: DaVinci Resolve 21 / 21.1

Джерело: матеріал №1 (твердження станом на 2026-09-18; зовнішні посилання — в inbox-файлі). Статус: довідка.

Перед використанням перевіряти `probe()` на конкретній машині: фічі залежать від версії та наявності Studio.

## Можливості, релевантні воркфлоу

- **IntelliSearch**: пошук за visual content, transcript і metadata окремо; обличчя; повертає релевантний сегмент усередині довгого кліпу.
- **Транскрипція**; у Studio AI-операції IntelliSearch і transcription доступні через scripting API.
- **Стабілізація**: smoothing, strength, crop, Camera Lock — контролюються окремо; не застосовувати сліпо до всього матеріалу, можна прибрати лише погане тремтіння, не роблячи кадр «бетонним».
- **Transform keyframes** — ручний контрольований рух через Position/Scale; **Dynamic Zoom** — м'який push-in/pull-out для статичного матеріалу.
- **Speed Warp** з режимом Better — якісніший retiming; застосовувати вибірково й перевіряти кадри після інтерполяції (руки, волосся, тканини, люди, що перетинаються, конфеті, швидкі танці).
- **Shot Match**: матчинг камер за кольором, контрастом, яскравістю.
- **Fairlight**: cleanup, Voice Isolation, automatic ducking музики під діалог.
- **AI UltraSharpen**: незначно soft / out-of-focus матеріал — rescue, не воскресіння.
- **AI Motion Deblur**: особливо корисний перед slow motion / freeze frame.
- **Scripting API (Python/Lua)**: Media Pool, створення таймлайнів, in/out, маркери.

## Колірний порядок

Технічна нормалізація перед creative look: correct input color space → white balance → exposure → contrast → skin tone → camera matching → creative look.

Усі кадри однієї сцени мають виглядати так, ніби існують в одному просторі. Один grade не копіюється сліпо на все відео. Skin tone — під особливим контролем.
