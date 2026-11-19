"""Make an mp3 of every word in dictations.json with Google's Hebrew voice (gTTS), so the page can play the word as
a file: an iPhone on silent plays a file like a video, while it mutes the browser's own voice (19.11). The same voice
as the family tablet's (family-tablet, /api/tts), so she hears the words alike on both; Microsoft's sounded muffled.
Only words that have no file yet are made. audio/index.json maps the text read to its file; a file's name comes from
its text and the voice, so a new voice makes new files and the old ones go."""
import hashlib, json, pathlib

from gtts import gTTS

VOICE = 'gtts-iw'
root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'audio'
out.mkdir(exist_ok=True)

texts = []
for d in json.loads((root / 'dictations.json').read_text(encoding='utf-8')):
    for w in d['words']:
        # what the device voice reads: the word, or its spelled-out reading when one is given
        t = w[2] if len(w) > 2 and w[2] else w[0]
        if t not in texts:
            texts.append(t)
made = {}
for t in texts:
    name = hashlib.sha1(f'{VOICE}|{t}'.encode('utf-8')).hexdigest()[:12] + '.mp3'
    if not (out / name).exists():
        gTTS(t, lang='iw').save(str(out / name))
        print('made', name, t)
    made[t] = name
for f in out.glob('*.mp3'):
    if f.name not in made.values():
        f.unlink()
(out / 'index.json').write_text(json.dumps(made, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
