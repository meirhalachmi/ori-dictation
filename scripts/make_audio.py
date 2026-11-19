"""Make an mp3 of every word in dictations.json with a Hebrew neural voice (edge-tts), so the page can play the
word as a file: an iPhone on silent plays a file like a video, while it mutes the browser's own voice (19.11).
Only words that have no file yet are made. audio/index.json maps the text read to its file."""
import asyncio, hashlib, json, pathlib

import edge_tts

VOICE, RATE = 'he-IL-HilaNeural', '-15%'
root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'audio'
out.mkdir(exist_ok=True)
index_path = out / 'index.json'
index = json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else {}


async def main():
    texts = []
    for d in json.loads((root / 'dictations.json').read_text(encoding='utf-8')):
        for w in d['words']:
            # what the device voice reads: the word, or its spelled-out reading when one is given
            t = w[2] if len(w) > 2 and w[2] else w[0]
            if t not in texts:
                texts.append(t)
    for t in texts:
        name = hashlib.sha1(t.encode('utf-8')).hexdigest()[:12] + '.mp3'
        if index.get(t) == name and (out / name).exists():
            continue
        await edge_tts.Communicate(t, VOICE, rate=RATE).save(str(out / name))
        index[t] = name
        print('made', name, t)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')


asyncio.run(main())
