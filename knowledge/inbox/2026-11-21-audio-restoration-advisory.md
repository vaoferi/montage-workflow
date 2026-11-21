Так. Я б тут уже **не шукав один чарівний denoiser**. Для твого запису потрібна комбінація: `target speaker extraction → speech separation → enhancement`. І хороша новина — безкоштовні варіанти реально є.

### Що я б тестував у такому порядку

| Місце | Інструмент | Агент сам? | Безкоштовність | Що реально дає |
|---|---|---|---|---|
| **1** | **ClearerVoice Studio / ClearVoice** | ✅ Так | ✅ Open-source | Найкраща ставка: denoise + поділ голосів + **витяг конкретної людини по губах/обличчю** |
| **2** | **Adobe Enhance Speech v2** | 🖐 Переважно руками | ✅ 30 хв/файл, 1 год/день | Дуже сильний one-click rescue тихого/далекого голосу, шуму й ревербу |
| **3** | **DeepFilterNet** | ✅ Так | ✅ Open-source | Консервативно чистить сирену, машини, гул; добре як перший/останній denoise |
| **4** | **SpeechBrain SepFormer / WHAM** | ✅ Так | ✅ Open-source | Спеціаліст саме на **кількох голосах + environmental noise** |
| **5** | **Resemble Enhance** | ✅ Так | ✅ Open-source | Агресивніше “відновлює” дуже поганий голос; rescue-mode |
| **6** | **ElevenLabs Voice Isolator** | 🖐 / API | ✅ ~10 хв на Free | Варто протестувати як proprietary benchmark |
| — | Auphonic | ✅ API / 🖐 | ✅ 2 год/міс | Хороший cleanup, але free output має jingle — тому не ставлю в основний pipeline |

## 🥇 1. ClearerVoice — сюди я б кинув агента першим

Оце найбільш цікаве.

ClearVoice зараз має готові pretrained-моделі для:

**`MossFormer2_SE_48K`** → speech enhancement  
**`MossFormer2_SS_16K`** → speech separation  
**`AV_MossFormer2_TSE_16K`** → **audio-visual target speaker extraction**  
**`MossFormer2_SR_48K`** → speech super-resolution. [GitHub](https://github.com/modelscope/ClearerVoice-Studio/blob/main/clearvoice/README.md?utm_source=chatgpt.com)

Встановлення буквально:

```bash
pip install clearvoice
```

Моделі завантажуються автоматично з Hugging Face під час inference. [GitHub](https://github.com/modelscope/ClearerVoice-Studio/blob/main/clearvoice/README.md?utm_source=chatgpt.com)

### Найцікавіше для нареченої

`AV_MossFormer2_TSE_16K` дивиться не просто на звук.

Він використовує **lip/face visual cue**, щоб зрозуміти:

> оцей рот зараз говорить → дай мені саме цей голос.

Конфіг офіційної pretrained-моделі прямо має `cue: lip`, ResNet18 для visual reference і MossFormer2 для audio. [GitHub](https://github.com/modelscope/ClearerVoice-Studio/blob/main/clearvoice/clearvoice/config/inference/AV_MossFormer2_TSE_16K.yaml?utm_source=chatgpt.com)

Тобто якщо камера бачить обличчя нареченої під час її слів, я б **обов'язково це спробував**.

Саме тут потенційно можна прибрати:

оператора  
+ сторонніх людей  
+ частину шуму

і залишити **її голос**.

Це вже не класичний noise remover.

### Якщо обличчя не видно

Тоді `MossFormer2_SS_16K`.

Він видає окремі stems:

```text
speaker_1.wav
speaker_2.wav
```

Офіційний example саме так його використовує. [GitHub](https://github.com/modelscope/ClearerVoice-Studio/blob/main/clearvoice/demo_Numpy2Numpy.py?utm_source=chatgpt.com)

У ClearerVoice їхній unified MossFormer2 на noisy WHAM! benchmark має **17.4 dB SI-SNR improvement**; для порівняння, у їхній же таблиці SepFormer — 14.4 dB. Це не гарантія результату саме на твоєму весіллі, але причина почати саме звідси є. [GitHub](https://github.com/modelscope/ClearerVoice-Studio/blob/main/clearvoice/README.md?utm_source=chatgpt.com)

[ClearerVoice-Studio на GitHub](https://github.com/modelscope/ClearerVoice-Studio?utm_source=chatgpt.com)

---

## 🥈 2. Adobe Enhance Speech v2 — я б прогнав усі 15 хвилин

Тут у тебе було неправильне припущення щодо ліміту.

**Free plan зараз: до 30 хвилин на один audio file, до 500 MB і максимум 1 година processing на день.**

Отже **15 хвилин заходять одним файлом**. [Adobe Help Center](https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-audio/frequently-asked-questions-about-enhance-speech.html?utm_source=chatgpt.com)

Adobe заявляє, що Enhance Speech v2 працює з:

background noise  
reverb  
chatter  
background music

і намагається витягувати hard-to-hear speech. [podcast.adobe.com](https://podcast.adobe.com/en/enhancespeech?utm_source=chatgpt.com)

### Але

Він не знає:

> наречена хороша, оператор поганий.

Оператор теж говорить людським голосом.

Тому Adobe — чудовий:

**enhancer**

але не ідеальний:

**speaker extractor**.

Я б просто кинув туди **всі 15 хвилин** і отримав candidate B.

[Adobe Enhance Speech v2](https://podcast.adobe.com/en/enhancespeech?utm_source=chatgpt.com)

---

## 🥉 3. DeepFilterNet — агентський робочий кінь

Не наймагічніший, зате дуже корисний.

Працює з **48 kHz full-band audio**, має CLI і може запускатися повністю локально:

```bash
deep-filter input.wav
```

Модель орієнтована саме на speech enhancement / environmental noise suppression. [GitHub](https://github.com/Rikorose/DeepFilterNet?utm_source=chatgpt.com)

Я б використовував його:

**або перед separation**, якщо сирена/гул заважають моделі розрізняти людей,

**або після separation**, якщо отриманий голос ще шумний.

Але не обов'язково обидва — інакше можна перетворити голос на MP3 із 2003-го.

---

## 4. SpeechBrain SepFormer-WHAM

Це спеціально цікавий fallback.

`sepformer-wham` навчений на **speech mixtures + environmental noise** і має готову pretrained модель. Її benchmark — **16.3 dB SI-SNRi** на WHAM!. [huggingface.co](https://huggingface.co/speechbrain/sepformer-wham?utm_source=chatgpt.com)

Встановлення:

```bash
pip install speechbrain
```

а далі Python може зробити:

```python
from speechbrain.inference.separation import SepformerSeparation

model = SepformerSeparation.from_hparams(
    source="speechbrain/sepformer-wham"
)

model.separate_file("input.wav")
```

Тобто агенту дуже легко дати це як **альтернативний separator**.

Я б не ставив його поперед ClearerVoice, але якщо MossFormer2 погано розділить наречену/оператора — обов'язково A/B.

---

## 5. Resemble Enhance — коли треба вже чаклувати 🧙

Тут починається справжня магія.

Resemble складається з:

**denoiser** → відділення speech від noise

і

**enhancer** → намагається відновлювати distortion та bandwidth голосу. [GitHub](https://github.com/resemble-ai/resemble-enhance?utm_source=chatgpt.com)

Локально:

```bash
pip install resemble-enhance
```

Тільки denoise:

```bash
resemble-enhance input output --denoise_only
```

Повний rescue:

```bash
resemble-enhance input output
```

### Чому лише №5

Бо для твого випадку **правдивість слів важливіша за красу голосу**.

Enhancer уже починає реконструювати signal.

Тому я дозволив би:

`denoise_only` широко,

а full Enhance тільки для найгірших фраз із порівнянням transcript:

```text
ORIGINAL transcription
vs
ENHANCED transcription
```

Якщо слова змінилися — викидаємо результат.

---

## 6. ElevenLabs Voice Isolator

Як proprietary контрольний тест — дуже цікаво.

На Free зараз дають **10 000 credits**, Voice Isolator коштує **1000 credits за хвилину**, тобто приблизно **10 хвилин**. Максимальний файл — 1 година / 500 MB. [ElevenLabs](https://elevenlabs.io/voice-isolator?utm_source=chatgpt.com)

Я б узяв **10 найгірших хвилин**, а не все весілля.

Він спеціально тренований:

speech ↔ background noise. [ElevenLabs](https://elevenlabs.io/docs/help-center/product/core-capabilities/voice-isolator/what-is-voice-isolator?utm_source=chatgpt.com)

Але знову:

**інший голос ≠ background noise.**

Тому cameraman може залишитися.

[ElevenLabs Voice Isolator](https://elevenlabs.io/voice-isolator?utm_source=chatgpt.com)

---

# Що я б зробив конкретно з твоїм файлом

Не проганяй відразу 15 хвилин через сім моделей.

Спочатку знайди **30–60 секунд “пекла”**:

```text
наречена говорить дуже тихо
+
оператор щось каже
+
сирена
+
машини
+
зал/реверб
```

Це твій **audio torture test**.

Після нього агент робить:

```text
A ORIGINAL

B ClearVoice SE 48k

C ClearVoice Speech Separation

D ClearVoice AV Target Speaker — Bride

E DeepFilterNet

F SpeechBrain SepFormer-WHAM

G Resemble denoise_only

H Resemble full enhance
```

Ти слухаєш **одну хвилину × 8 варіантів**, а не 15 хвилин × 8.

І вже переможців застосовуєте по всьому матеріалу.

---

# 🔥 А найцікавіший pipeline я б перевірив такий

Для нареченої:

```text
CAMERA VIDEO + AUDIO
        ↓
AV_MossFormer2_TSE_16K
        ↓
BRIDE ONLY 16 kHz
        ↓
MossFormer2_SR_48K
        ↓
легкий DeepFilterNet / Resolve cleanup
        ↓
EQ + compression + room tone
        ↓
DaVinci
```

Тобто модель спочатку **дивиться на наречену**, дістає її голос, а потім інша модель намагається повернути ширший спектр.

Оце я б назвав найближчим безкоштовним варіантом до твоєї “магічної палички”.

Для пастора:

```text
PASTOR FACE
→ AV Target Speaker Extraction
→ enhancement
```

Для нареченого так само.

А потім агент збирає три cleaned tracks назад по таймкодах.

Це вже набагато розумніше, ніж намагатися одним denoiser'ом врятувати весь soundtrack.

---

## Ось prompt, який я б прямо зараз кинув агенту

У нас є критична проблема wedding project:

original dedicated audio track втрачена.

Є тільки camera audio.

Якість дуже погана:

- bride чути дуже тихо;
- groom чути краще;
- pastor чути краще;
- cameraman та інші люди іноді говорять поверх потрібної мови;
- є сирена;
- автомобілі;
- постійний background hum;
- room/reverb;
- частина clicks уже очищена.

Мета:

НЕ просто зробити звук чистішим.

Мета — максимально відновити intelligibility реальних слів bride, groom і pastor та, де можливо, відділити їх від сторонніх голосів і шуму.

## Критичне правило

Original audio не змінювати.

Усі outputs зберігати окремо.

AI enhancement не має права непомітно змінювати фактичні слова.

Якщо reconstructed/enhanced audio дає інший transcript, ніж original або інші processing candidates, позначай `MANUAL_REVIEW`.

---

## PHASE 1 — TORTURE TEST

Не обробляй одразу всі ~15 хвилин.

Знайди 30–60 секунд найбільш проблемного фрагмента, де одночасно присутні:

- тихий голос bride;
- environmental noise;
- siren/car/hum/reverb;
- бажано сторонній speaker/cameraman.

Це canonical torture sample.

Збережи:

`audio_test/00_original.wav`

48 kHz PCM WAV, без destructive normalization.

---

## PHASE 2 — INSTALL / VERIFY CLEARVOICE

Перевір актуальний official repository:

`modelscope/ClearerVoice-Studio`

Встанови ClearVoice із current official instructions.

Базовий пакет:

`pip install clearvoice`

Не використовуй застарілий syntax без перевірки current README.

Протестуй доступні pretrained models:

### Candidate 1

`MossFormer2_SE_48K`

Task:

`speech_enhancement`

Output:

`01_clearvoice_se48.wav`

### Candidate 2

`MossFormer2_SS_16K`

Task:

`speech_separation`

Збережи всі generated speaker stems:

`02_clearvoice_ss_speaker1.wav`
`02_clearvoice_ss_speaker2.wav`

Не припускай автоматично, хто є хто.

Визнач speaker за слухом + video + transcript.

---

## PHASE 3 — AUDIO-VISUAL TARGET SPEAKER EXTRACTION

Це високопріоритетний експеримент.

Якщо у відео видно обличчя/губи:

- bride;
- groom;
- pastor,

протестуй:

`AV_MossFormer2_TSE_16K`

Task:

`target_speaker_extraction`

Мета — використовувати visual lip cue для extraction конкретного active speaker.

Створи окремі candidate outputs:

`03_tse_bride.wav`
`03_tse_groom.wav`
`03_tse_pastor.wav`

Не запускай це сліпо на segment, якщо target face/lips не видно достатньо добре.

Для кожного output перевір:

- чи залишився потрібний speaker;
- чи прибрані сторонні speakers;
- чи не втрачено слова;
- чи немає pumping / metallic artifacts.

---

## PHASE 4 — SPEECH SUPER RESOLUTION

Якщо TSE 16 kHz добре ізолював speaker, але звучить вузько:

протестуй current ClearVoice speech super-resolution model:

`MossFormer2_SR_48K`

Створи candidate:

`04_bride_tse_sr48.wav`

Не приймай його автоматично.

A/B:

TSE 16k
vs
TSE → SR48.

---

## PHASE 5 — DEEPFILTERNET

Встанови current official DeepFilterNet.

Створи candidate на original torture sample:

`05_deepfilternet.wav`

Також за потреби протестуй DeepFilterNet ПІСЛЯ speaker extraction:

`05_bride_tse_deepfilter.wav`

Не роби double-denoise, якщо він створює artifacts.

---

## PHASE 6 — SPEECHBRAIN SEPARATION

Встанови SpeechBrain.

Протестуй current pretrained:

`speechbrain/sepformer-wham`

або current better official SpeechBrain pretrained separation model, якщо documentation показує явно кращий варіант для noisy speech mixtures.

Створи:

`06_sepformer_source1.wav`
`06_sepformer_source2.wav`

Якщо є appropriate 3-speaker pretrained model і реальний segment має 3 overlapping speakers, можеш окремо протестувати його.

Не тренуй нову модель.

---

## PHASE 7 — RESEMBLE ENHANCE

Встанови current official:

`resemble-ai/resemble-enhance`

Спочатку:

`--denoise_only`

Output:

`07_resemble_denoise.wav`

Потім окремо:

full enhancement

Output:

`08_resemble_full.wav`

Full enhancement вважай EXPERIMENTAL.

Він не може автоматично стати production audio.

---

## PHASE 8 — TRANSCRIPTION CONSENSUS

Для torture sample отримай transcript мінімум для:

- ORIGINAL;
- ClearVoice SE;
- best separated/TSE output;
- DeepFilterNet;
- Resemble denoise;
- Resemble full.

Використовуй current working transcription pipeline проєкту.

Порівняй words.

Якщо cleaned versions допомагають стабільно розпізнати слова, які original transcription не розпізнав, це позитивний сигнал.

Якщо один enhancer видає слова, яких немає в інших candidates:

познач:

`POSSIBLE_AI_SPEECH_ARTIFACT`

і не використовуй його без manual review.

---

## PHASE 9 — REPORT

Не обирай переможця тільки за автоматичним metric.

Створи папку:

`audio_test/candidates/`

і збережи всі candidates синхронізованими до однакового start time і duration.

Створи короткий report:

| Candidate | Noise removal | Bride intelligibility | Other speakers removed | Naturalness | Artifacts | Transcript confidence |
|---|---|---|---|---|---|---|

Не вигадуй оцінки, якщо candidate реально не був прослуханий або перевірений доступним способом.

Особливо відміть:

1. найкращий варіант для bride;
2. найкращий для groom;
3. найкращий для pastor;
4. найкращий conservative cleanup;
5. найкращий aggressive rescue.

Після torture test НЕ обробляй повні 15 хвилин автоматично.

Спочатку зафіксуй результати і визнач, який pipeline має сенс масштабувати.

## PRIORITY

Найбільший пріоритет:

ClearVoice Audio-Visual Target Speaker Extraction.

Якщо face/lip cue працює добре, побудуй подальший pipeline навколо нього.

Наша задача — не зробити recording стерильним.

Наша задача — врятувати реальні слова людей.

**Я б почав буквально з ClearerVoice TSE + Adobe.** Якщо ClearerVoice дійсно витягне наречену по губах — питання майже вирішене. Якщо ні, Adobe дає тобі дуже дешевий у сенсі часу шанс одним файлом перевірити, скільки можна витягнути зі всіх 15 хвилин.

**Пастка:** не дай агенту “покращити” голос так, що він стане красивішим, але слова — іншими. Для весілля краще трохи гірший звук із реальною фразою нареченої, ніж ідеальний AI-голос, який сказав те, чого вона не казала.