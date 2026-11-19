"""Samples for compare.html: the same words in each candidate voice, to pick the dictation's voice by ear (19.11)."""
import asyncio, json, pathlib

import edge_tts
from gtts import gTTS

root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'compare'
out.mkdir(exist_ok=True)
WORDS = ['שָׂמַח', 'גַנָן', 'הָיָה', 'שָׁתַל', 'אַבָּא', 'אבא']
# edge-tts gives 24kHz at 48kbps unless asked otherwise; 96kbps is the best it gave (19.11)
import aiohttp
_send = aiohttp.ClientWebSocketResponse.send_str
async def send_str(self, data, *a, **k):
    return await _send(self, data.replace('audio-24khz-48kbitrate-mono-mp3', 'audio-24khz-96kbitrate-mono-mp3'), *a, **k)
aiohttp.ClientWebSocketResponse.send_str = send_str

VOICES = [
    ('google', 'גוגל (כמו היום, כמו בטאבלט)', None),
    ('hila', 'מיקרוסופט — הילה', ('he-IL-HilaNeural', '+0%')),
    ('hila-slow', 'מיקרוסופט — הילה, לאט', ('he-IL-HilaNeural', '-15%')),
    ('avri', 'מיקרוסופט — אברי', ('he-IL-AvriNeural', '+0%')),
    ('avri-slow', 'מיקרוסופט — אברי, לאט', ('he-IL-AvriNeural', '-15%')),
]


async def main():
    for key, _, edge in VOICES:
        for i, w in enumerate(WORDS):
            path = out / f'{key}-{i}.mp3'
            if edge:
                await edge_tts.Communicate(w, edge[0], rate=edge[1]).save(str(path))
            else:
                gTTS(w, lang='iw').save(str(path))
            print('made', path.name, w)
    (out / 'list.json').write_text(json.dumps({'words': WORDS, 'voices': [[k, n] for k, n, _ in VOICES]},
                                              ensure_ascii=False) + '\n', encoding='utf-8')


asyncio.run(main())
