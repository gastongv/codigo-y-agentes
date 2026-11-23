"""Hornea los planos 4K de Mixkit (broll/m<id>.mp4) a assets/clips/<nombre>.mp4 (1080x1920, 30 fps).

Recorte vertical, color vivo (sin look de cine: el spot es luminoso) y un cuadro de origen por cuadro de salida:
los originales de 24 o 25 fps quedan un 20-25 % más rápidos, sin cuadros repetidos.
Uso: python fuente/hornear.py [nombre ...]   (lee trabajo/montaje.json)
"""
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAJA = 0x00004000 if os.name == "nt" else 0
m = json.load(open(os.path.join(RAIZ, "trabajo", "montaje.json"), encoding="utf-8"))
os.makedirs(os.path.join(RAIZ, "assets", "clips"), exist_ok=True)

for p in m["planos"]:
    if sys.argv[1:] and p["n"] not in sys.argv[1:]:
        continue
    # original: id de Mixkit en broll/, o una ruta relativa a videos/
    src = (os.path.join(os.path.dirname(RAIZ), p["vid"]) if "/" in p["vid"]
           else os.path.join(RAIZ, "broll", "m%s.mp4" % p["vid"]))
    out = os.path.join(RAIZ, "assets", "clips", p["n"] + ".mp4")
    cuadros = int(round((p["b"] - p["a"]) * 30)) + 12
    gamma, sat = p["gamma"], p["sat"]
    vf = ("crop=ih*9/16:ih:(iw-ih*9/16)*%s:0,scale=1080:1920:flags=lanczos,setpts=N/30/TB,"
          "eq=gamma=%s:contrast=1.06:saturation=%s,unsharp=5:5:0.5:5:5:0,format=yuv420p,"
          "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709" % (p["pos"], gamma, sat))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(p["ent"]), "-i", src,
                    "-vf", vf, "-frames:v", str(cuadros), "-r", "30", "-an", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "14", "-g", "15", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-threads", "6", out], check=True, creationflags=BAJA)
    print(p["n"], cuadros, "cuadros")
