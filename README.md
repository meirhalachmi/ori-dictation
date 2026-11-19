# Ori's dictation practice

One page (`index.html`), published with GitHub Pages. The dictations are in `dictations.json`,
newest first:

```json
{"id": "2026-11-18", "title": "הכתבה חדשה, 18.11", "date": "2026-11-22", "when": "ביום ראשון", "words": [
  ["גַנָן", "👨‍🌾"], ["אַבָּא", "👨", "אבא"]
]}
```

- `words`: the teacher's words as written (with niqqud; the page splits them into letter + nikud),
  a picture, and optionally what the device voice reads instead, for a word it stresses wrong (or
  record the word in the app).
- `date`: the day of the dictation in class (`null` if unknown). The family tablet reads this file
  and shows the coming dictation on Ori's school screen, with a button that opens this page inside
  the tablet at `?d=<id>`; the page then tells the tablet her stars (`postMessage`).
- `when`: said in the closing words of the last level ("ביום ראשון בכיתה עושים בדיוק אותו דבר").
- Audio: on every change to `dictations.json` a GitHub Action (`.github/workflows/audio.yml`) reads each word with a
  Hebrew neural voice (`scripts/make_audio.py`, edge-tts) into `audio/`, and the page plays those files: an iPhone on
  silent mutes the browser's own voice but plays a file. A parent's recording still comes first, and a word with no
  file yet falls back to the device voice. The `tts` reading above is used for the file too.
