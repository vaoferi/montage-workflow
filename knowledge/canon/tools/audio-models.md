# Інструменти: аудіо-відновлення та розділення мовлення

Джерело: матеріал №5 (твердження станом на 2026-09 → 2026-11; зовнішні посилання — в inbox-файлі). Статус: довідка.

Усі версії, ліміти й API перевіряти перед використанням (`process/agent-discipline.md`: актуальність інформації).

## ClearerVoice / ClearerVoice-Studio (open-source)

Pretrained-моделі:

- `MossFormer2_SE_48K` — speech enhancement;
- `MossFormer2_SS_16K` — speech separation (окремі stems `speaker_1.wav`, `speaker_2.wav`);
- `AV_MossFormer2_TSE_16K` — audio-visual target speaker extraction (lip/face cue; ResNet18 для visual reference + MossFormer2 для аудіо);
- `MossFormer2_SR_48K` — speech super-resolution.

Встановлення: `pip install clearvoice`; моделі завантажуються автоматично з Hugging Face під час inference.

Benchmark (їхня таблиця): unified MossFormer2 на noisy WHAM! — 17.4 dB SI-SNR improvement; SepFormer — 14.4 dB. Не гарантія результату на конкретному матеріалі, але причина почати звідси.

## Adobe Enhance Speech v2

One-click enhancer для тихого/далекого голосу, шуму, ревербу, chatter, background music. Ліміти free (за заявою Adobe): до 30 хв на один файл, до 500 MB, до ~1 години processing на день. Enhancer, не speaker extractor.

## DeepFilterNet (open-source)

48 kHz full-band; CLI `deep-filter input.wav`; консервативне придушення environmental noise. Використовувати до або після separation, не обидва без потреби.

## SpeechBrain SepFormer-WHAM (open-source)

`speechbrain/sepformer-wham` — навчений на speech mixtures + environmental noise; benchmark 16.3 dB SI-SNRi на WHAM!; `pip install speechbrain`; `SepformerSeparation.from_hparams(...)`. Fallback-separator для A/B проти MossFormer2.

## Resemble Enhance (open-source)

Denoiser + enhancer. `resemble-enhance input output --denoise_only` — консервативно; повний enhance реконструює signal — experimental, обов'язкове порівняння transcript.

## ElevenLabs Voice Isolator (proprietary)

Speech ↔ background noise. Free: ~10 000 credits, ~1000 credits/хв ≈ 10 хв; max 1 год / 500 MB. Інший людський голос ≠ noise — cameraman може залишитися. Використовувати як benchmark на найгірших хвилинах, не на всьому матеріалі.

## Auphonic (service)

Хороший cleanup, але free output має jingle → не в основний пайплайн.
