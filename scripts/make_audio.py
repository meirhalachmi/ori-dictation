"""Make an mp3 of every word in dictations.json with a Hebrew neural voice (edge-tts), so the page can play the
word as a file: an iPhone on silent plays a file like a video, while it mutes the browser's own voice (19.11).
Only words that have no file yet are made. audio/index.json maps the text read to its file.

edge-tts asks for 24kHz at 48kbps, which sounds thin on a phone (19.11); ask for the best format the service gives.
A file's name comes from its text and the settings, so new settings make new files and the old ones go."""
import asyncio, hashlib, json, pathlib

import aiohttp
import edge_tts

VOICE, RATE = 'he-IL-HilaNeural', '-15%'
DEFAULT = 'audio-24khz-48kbitrate-mono-mp3'
FORMATS = ['audio-48khz-192kbitrate-mono-mp3', 'audio-48khz-96kbitrate-mono-mp3',
           'audio-24khz-160kbitrate-mono-mp3', 'audio-24khz-96kbitrate-mono-mp3', DEFAULT]
fmt = DEFAULT

# edge-tts has the format fixed in its request, so swap it on the way out
_send = aiohttp.ClientWebSocketResponse.send_str
async def send_str(self, data, *a, **k):
    return await _send(self, data.replace(DEFAULT, fmt), *a, **k)
aiohttp.ClientWebSocketResponse.send_str = send_str

root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'audio'
out.mkdir(exist_ok=True)
index_path = out / 'index.json'
index = json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else {}


async def read(t, path):
    await edge_tts.Communicate(t, VOICE, rate=RATE).save(str(path))
    if not path.exists() or path.stat().st_size < 1000:
        raise RuntimeError('no audio')


async def main():
    global fmt
    texts = []
    for d in json.loads((root / 'dictations.json').read_text(encoding='utf-8')):
        for w in d['words']:
            # what the device voice reads: the word, or its spelled-out reading when one is given
            t = w[2] if len(w) > 2 and w[2] else w[0]
            if t not in texts:
                texts.append(t)
    probe = out / 'probe.mp3'
    for fmt in FORMATS:
        try:
            await read(texts[0], probe)
            break
        except Exception as e:
            print('format', fmt, 'refused:', e)
    probe.unlink(missing_ok=True)
    print('format', fmt)
    made = {}
    for t in texts:
        name = hashlib.sha1('|'.join([VOICE, RATE, fmt, t]).encode('utf-8')).hexdigest()[:12] + '.mp3'
        if not (out / name).exists():
            await read(t, out / name)
            print('made', name, t)
        made[t] = name
    for f in out.glob('*.mp3'):
        if f.name not in made.values():
            f.unlink()
    index_path.write_text(json.dumps(made, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')


asyncio.run(main())
