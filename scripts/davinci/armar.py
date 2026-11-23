"""Arma el spot a partir del render de la imagen (renders/imagen.mp4) y de trabajo/montaje.json.

Salidas:
  media/     plano-NN-<nombre>.mp4 (un archivo por plano, con el producto y los textos ya puestos),
             voz-vN.wav, musica.wav, sfx-NN-<nombre>.wav (con el volumen de la mezcla aplicado)
  entrega/   <nombre>.mp4 (el spot terminado) y subtitulos.srt
  trabajo/   plan-mcp.json (clips para el autor sin conexión del MCP de DaVinci Resolve)
"""
import json
import os
import subprocess

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA, ENTREGA, TRABAJO = (os.path.join(RAIZ, d) for d in ("media", "entrega", "trabajo"))
MUSICA = os.path.join(os.path.dirname(RAIZ), "griftia-pro", "assets", "bgm", "digital-lemonade.mp3")
MUSICA_DESDE, VOL_MUSICA = 0.0, 0.34
BAJA = 0x00004000 if os.name == "nt" else 0
m = json.load(open(os.path.join(TRABAJO, "montaje.json"), encoding="utf-8"))
FPS, DUR = m["fps"], m["dur"]
fr = lambda t: int(round(t * FPS))


def ffmpeg(args, hilos=4):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-threads", str(hilos)] + args,
                   check=True, creationflags=BAJA)


def dur_de(ruta):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                                capture_output=True, text=True).stdout)


def tc(t):
    ms = int(round(t * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)


for d in (MEDIA, ENTREGA):
    os.makedirs(d, exist_ok=True)
imagen = os.path.join(RAIZ, "renders", "imagen.mp4")

# --- Planos: un archivo por corte, exacto al cuadro ---
planos = []
for i, p in enumerate(m["planos"], 1):
    a, b = fr(p["a"]), fr(p["b"])
    out = os.path.join(MEDIA, "plano-%02d-%s.mp4" % (i, p["n"]))
    ffmpeg(["-i", imagen, "-vf", "trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS" % (a, b), "-an", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "13", "-pix_fmt", "yuv420p", "-g", "15", out])
    planos.append({"n": p["n"], "ruta": out, "rec": a, "dur": b - a})

# --- Audios separados (48 kHz estéreo) ---
voces = []
for v in m["voces"]:
    out = os.path.join(MEDIA, "voz-%s.wav" % v["id"])
    ffmpeg(["-i", os.path.join(RAIZ, "voz", v["id"] + ".mp3"), "-t", "%.3f" % v["dur"],
            "-af", "afade=t=out:st=%.3f:d=0.08" % (v["dur"] - 0.08), "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", out])
    voces.append({"id": v["id"], "ruta": out, "ini": v["t0"], "dur": v["dur"], "texto": v["texto"], "pal": v["pal"]})
musica = os.path.join(MEDIA, "musica.wav")
ffmpeg(["-ss", str(MUSICA_DESDE), "-i", MUSICA, "-t", "%.3f" % DUR,
        "-af", "volume=%s,afade=t=in:st=0:d=0.25,afade=t=out:st=%.3f:d=1.3" % (VOL_MUSICA, DUR - 1.3),
        "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", musica])
sfx = []
for i, (nombre, cuando, vol) in enumerate(m["sfx"], 1):
    out = os.path.join(MEDIA, "sfx-%02d-%s.wav" % (i, nombre))
    ffmpeg(["-i", os.path.join(RAIZ, "assets", "sfx", nombre + ".mp3"), "-af", "volume=%s" % vol,
            "-ar", "48000", "-ac", "2", "-c:a", "pcm_s24le", out])
    sfx.append({"n": nombre, "ruta": out, "ini": cuando, "dur": dur_de(out)})

# --- Subtítulos (.srt): una idea por línea, cortando después de cada coma o punto ---
subs = []
for v in voces:
    visibles, grupo = v["texto"].split(), []
    pal = v["pal"] if len(v["pal"]) == len(visibles) else None
    for i, palabra in enumerate(visibles):
        grupo.append(i)
        if palabra.endswith((",", ".")) or i == len(visibles) - 1:
            if pal:
                a, b = pal[grupo[0]]["start"], pal[grupo[-1]]["end"]
            else:
                a, b = v["dur"] * grupo[0] / len(visibles), v["dur"] * (grupo[-1] + 1) / len(visibles)
            subs.append([" ".join(visibles[j] for j in grupo), v["ini"] + a, v["ini"] + b + 0.1])
            grupo = []
for i in range(len(subs) - 1):
    subs[i][2] = min(subs[i][2], subs[i + 1][1] - 0.02)
with open(os.path.join(ENTREGA, "subtitulos.srt"), "w", encoding="utf-8") as f:
    for i, (texto, a, b) in enumerate(subs, 1):
        f.write("%d\n%s --> %s\n%s\n\n" % (i, tc(a), tc(b), texto))

# --- Plan para el MCP de DaVinci (pista de video + pista de voz) y datos para otio_final.py ---
clips = [{"path": p["ruta"], "name": os.path.basename(p["ruta"]), "media_type": "video", "record_frame": p["rec"],
          "start_frame": 0, "end_frame": p["dur"], "fps": FPS, "media_start_tc_frame": 0} for p in planos]
clips += [{"path": v["ruta"], "name": "voz " + v["id"], "media_type": "audio", "record_frame": fr(v["ini"]),
           "start_frame": 0, "end_frame": fr(v["dur"]), "fps": FPS, "media_start_tc_frame": 0} for v in voces]
json.dump(clips, open(os.path.join(TRABAJO, "plan-mcp.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"nombre": m["nombre"], "fps": FPS, "total": fr(DUR),
           "musica": {"ruta": musica, "rec": 0, "dur": fr(DUR)},
           "sfx": [{"n": s["n"], "ruta": s["ruta"], "rec": fr(s["ini"]), "dur": fr(s["dur"])} for s in sfx]},
          open(os.path.join(TRABAJO, "pistas-extra.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# --- El spot terminado: la imagen con la mezcla ---
audios = [(v["ruta"], v["ini"]) for v in voces] + [(musica, 0)] + [(s["ruta"], s["ini"]) for s in sfx]
args, filtros, mezcla = ["-i", imagen], [], []
for j, (ruta, cuando) in enumerate(audios):
    args += ["-i", ruta]
    ms = max(0, int(round(cuando * 1000)))
    filtros.append("[%d:a]adelay=%d|%d[a%d]" % (j + 1, ms, ms, j))
    mezcla.append("[a%d]" % j)
filtros.append("%samix=inputs=%d:normalize=0:duration=longest,volume=1.5,alimiter=limit=0.94,atrim=end=%.3f[aout]"
               % ("".join(mezcla), len(audios), DUR))
salida = os.path.join(ENTREGA, m["nombre"] + ".mp4")
ffmpeg(args + ["-filter_complex", ";".join(filtros), "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow",
               "-crf", "17", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-g", "60", "-r", str(FPS),
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", salida])
print("planos: %d | voces: %d | efectos: %d | subtítulos: %d" % (len(planos), len(voces), len(sfx), len(subs)))
print("spot:", salida, "%.1f MB" % (os.path.getsize(salida) / 1e6))
