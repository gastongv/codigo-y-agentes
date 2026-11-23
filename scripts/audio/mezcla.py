"""Mezcla de audio del comercial 3D: voz (Dalia), música "Inspired" (Kevin MacLeod, CC BY 4.0) y efectos.

Uso: python mezcla.py  → audio/mezcla.wav (34,5 s, 48 kHz estéreo)
La música queda ~10 dB por debajo de la voz y se baja unos 6 dB más mientras se habla (sidechain),
así se escucha pero no tapa lo que se dice.
"""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(AQUI, "..", "griftia-hw1-peluqueria", "assets", "sfx")
MUSICA = os.path.join(AQUI, "..", "griftia-pro", "assets", "bgm", "inspired.mp3")
TOTAL = 34.5
V = {"vo-01": 0.4, "vo-02": 3.55, "vo-03": 5.8, "vo-04": 8.8, "vo-05": 13.0, "vo-06": 18.3, "vo-07": 21.8, "vo-08": 27.2}
LINES = {l["id"]: l for l in json.load(open(os.path.join(AQUI, "voz", "lines.json"), encoding="utf-8"))}
W = lambda i, k: V[i] + LINES[i]["words"][k]["start"]

tGriftia, tInst, tAgenda, tPrecios = W("vo-04", 2), W("vo-05", 1), W("vo-05", 7), W("vo-05", 14)
tToma, tHor, t24, tVisita = W("vo-06", 7), W("vo-07", 3), W("vo-07", 4), W("vo-08", 5)
# (archivo, inicio, volumen[, desde, duración]) — desde/duración recortan el archivo
EFECTOS = [
    *[("ping", t, 0.22) for t in (0.7, 1.3, 1.9, 2.6, 3.3, 4.0)],
    ("whoosh-short", 3.5, 0.35), ("whoosh", 5.75, 0.4),
    # el golpe va en el corte (8,62 s), antes de que hable la voz, y bajito: no tapa "Conocé a GriftIA"
    ("riser", 7.82, 0.22, 9.23, 0.8), ("impact-bass-1", 8.6, 0.26), ("sparkle", tGriftia + 0.65, 0.18),
    *[("pop", 9.6 + i * 0.28, 0.18) for i in range(6)],
    ("whoosh-short", 12.95, 0.35), ("typing", 13.3, 0.18), ("pop", tInst, 0.3), ("chime", tAgenda - 0.1, 0.3), ("pop", tPrecios - 0.1, 0.3),
    ("whoosh-short", 15.55, 0.35), *[("pop", t, 0.28) for t in (15.7, 16.05, 16.4)],
    ("whoosh", 18.25, 0.35), ("key-press", tToma - 0.02, 0.5), ("chime", tToma + 0.08, 0.3),
    ("whoosh-short", 21.75, 0.35), ("whoosh-short", tHor - 0.3, 0.35), ("whoosh", t24 - 0.3, 0.4), ("impact-bass-2", t24 - 0.25, 0.4),
    ("whoosh-cinematic", 27.0, 0.3, 0, 2.0), ("impact-bass-2", 27.5, 0.5), ("sparkle", 28.0, 0.35), ("pop", tVisita - 0.1, 0.4),
]

ins, filt, voces, efectos = [], [], [], []
for i, (vid, t) in enumerate(V.items()):
    ins += ["-i", os.path.join(AQUI, "voz", f"{vid}.mp3")]
    filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(t * 1000)}|{int(t * 1000)}[v{i}]")
    voces.append(f"[v{i}]")
n = len(V)
ins += ["-i", MUSICA]
filt.append(f"[{n}:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=-10dB,afade=t=in:d=0.6,afade=t=out:st={TOTAL - 2.5}:d=2.5[mus]")
for j, (nombre, t, vol, *rec) in enumerate(EFECTOS):
    k = n + 1 + j
    ins += ["-i", os.path.join(SFX, f"{nombre}.mp3")]
    corte = f"atrim={rec[0]}:{rec[0] + rec[1]},asetpts=PTS-STARTPTS,afade=t=out:st={max(0, rec[1] - 0.25)}:d=0.25," if rec else ""
    filt.append(f"[{k}:a]{corte}aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={int(t * 1000)}|{int(t * 1000)}[s{j}]")
    efectos.append(f"[s{j}]")
filt.append(f"{''.join(voces)}amix=inputs={len(voces)}:normalize=0:duration=longest,apad=whole_dur={TOTAL}[voz]")
filt.append("[voz]asplit=2[voz1][key]")
filt.append("[mus][key]sidechaincompress=threshold=0.03:ratio=3:attack=30:release=450:makeup=1[musd]")
filt.append(f"{''.join(efectos)}amix=inputs={len(efectos)}:normalize=0:duration=longest[fx]")
filt.append(f"[voz1][musd][fx]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.89:level=disabled[out]")
os.makedirs(os.path.join(AQUI, "audio"), exist_ok=True)
out = os.path.join(AQUI, "audio", "mezcla.wav")
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(filt), "-map", "[out]", "-t", str(TOTAL), "-ar", "48000", out], check=True)
print("listo:", out)
