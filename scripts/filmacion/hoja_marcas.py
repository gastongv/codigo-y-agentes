# Hojas para buscar marcas y juzgar el foco: 3 cuadros de cada plano, desde el 4K original con el mismo recorte vertical.
# Uso: python fuente/hoja_marcas.py  (desde la carpeta del proyecto). Lee la tabla PLANOS de fuente/hornear.py
# (acá, hornear_cine.py) sin correrlo. Requiere Pillow.
import ast
import os
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(RAIZ, "fuente", "hornear.py"), encoding="utf8").read()
PLANOS = ast.literal_eval(re.search(r"PLANOS = (\{.*?\n\})", src, re.S).group(1))
SALIDA = os.path.join(RAIZ, "revision", "marcas")
os.makedirs(SALIDA, exist_ok=True)
A, H, POR_HOJA = 330, 587, 12
fuente = ImageFont.load_default(size=24)
cuadros = []
for nombre, (vid, entrada, dur, pos, *_) in PLANOS.items():
    for k, t in enumerate((entrada + 0.1, entrada + dur / 2, entrada + dur - 0.1)):
        p = os.path.join(SALIDA, f"{nombre}-{k}.jpg")
        if not os.path.exists(p):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", "-ss", str(t), "-i", os.path.join(RAIZ, "broll", f"m{vid}.mp4"),
                            "-frames:v", "1", "-vf", f"crop=ih*9/16:ih:(iw-ih*9/16)*{pos}:0,scale={A}:{H}:flags=lanczos,eq=gamma=1.35", "-q:v", "3", p], check=True)
        cuadros.append((f"{nombre} {t:.1f}", p))
for h in range(0, len(cuadros), POR_HOJA):
    grupo = cuadros[h:h + POR_HOJA]
    hoja = Image.new("RGB", (6 * (A + 4), 2 * (H + 4)))
    d = ImageDraw.Draw(hoja)
    for i, (rot, p) in enumerate(grupo):
        x, y = (i % 6) * (A + 4), (i // 6) * (H + 4)
        hoja.paste(Image.open(p), (x, y))
        d.rectangle([x, y, x + 200, y + 30], fill=(0, 0, 0))
        d.text((x + 4, y + 2), rot, font=fuente, fill=(255, 230, 0))
    hoja.save(os.path.join(RAIZ, "revision", f"marcas-{h // POR_HOJA + 1}.jpg"), quality=90)
print("hojas", (len(cuadros) + POR_HOJA - 1) // POR_HOJA)
