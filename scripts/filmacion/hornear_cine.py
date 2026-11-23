# Hornea los planos de broll/ a assets/clips/: recorte 9:16 sin perder el detalle del 4K, exposición por plano,
# Vision3 500T mezclado al 40 % (piel natural, sombras abiertas), nitidez suave, viñeta mínima y grano fino.
# Sin GPU y con pocos hilos, para poder seguir usando la PC mientras hornea.
# La tabla de color (LUT) viene con la skill ghost-editor; sirve cualquier .cube de película.
# Uso: python fuente/hornear.py [nombres...]  (sin nombres hornea todos)
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BROLL = os.path.join(RAIZ, "broll")
SALIDA = os.path.join(RAIZ, "assets", "clips")
os.makedirs(SALIDA, exist_ok=True)
LUT = os.path.expanduser("~/.claude/skills/ghost-editor/library/luts/vision3_500t.cube").replace("\\", "/").replace(":", "\\:")
HILOS = "4"
MEZCLA_LUT = 0.40
# El ancho de 1216 es el recorte vertical de un 4K: el empuje de cámara del video trabaja sobre detalle real, sin agrandar.
ANCHO, ALTO = 1216, 2160
# nombre: (id Mixkit, entrada s, duración s, posición horizontal 0-1, gamma, saturación, desenfoque[, recorte arriba, recorte abajo])
# Los recortes sacan carteles y emblemas de los bordes; el 4K da margen sin perder nitidez.
PLANOS = {
    "ciudad":     ("1772",  1.0, 2.3, 0.50, 1.00, 1.08, 0, 0.0, 0.15),
    "oficina":    ("39839", 2.0, 3.0, 0.30, 1.38, 0.96, 0),
    "barbero":    ("357",   0.5, 1.4, 0.50, 1.12, 1.00, 0),
    "dentista":   ("12145", 3.0, 1.3, 0.42, 1.00, 1.00, 0),
    "gimnasio":   ("52102", 8.9, 1.3, 0.50, 1.25, 1.00, 0, 0.08, 0.0),
    "reposteria": ("50017", 3.0, 1.3, 0.50, 1.00, 1.04, 0),
    "taller":     ("41933", 3.0, 1.1, 0.50, 1.40, 1.00, 0),
    "empresa":    ("4547",  5.0, 1.9, 0.50, 1.02, 1.02, 0),
    "rotonda":    ("1615",  3.0, 1.5, 0.50, 1.20, 1.04, 0),
    "ocaso":      ("4808",  2.0, 1.6, 0.30, 1.00, 1.00, 0),
    "fondo-a":    ("4813",  2.0, 7.5, 0.50, 1.00, 1.00, 8),
    "piensa":     ("39838", 3.0, 2.3, 0.30, 1.30, 0.96, 0),
    "espresso":   ("3571",  3.0, 2.2, 0.50, 1.06, 1.00, 0),
    "mensajes":   ("51122", 2.0, 2.4, 0.50, 1.06, 1.00, 0),
    "flores":     ("4742",  2.0, 2.7, 0.50, 1.02, 1.04, 0),
    "sillones":   ("43236", 2.0, 2.9, 0.50, 1.45, 1.00, 0),
    "ciudad2":    ("1616",  2.0, 1.7, 0.50, 1.10, 1.06, 0),
    "torres":     ("283",   2.0, 2.3, 0.50, 1.30, 1.04, 0),
    "consumo":    ("4804",  2.0, 4.9, 0.50, 1.00, 1.02, 0),
    "plan":       ("4805",  2.0, 3.7, 0.50, 1.10, 1.00, 0),
    "cierre":     ("3134",  0.5, 6.8, 0.50, 1.22, 1.06, 0),
}


def filtro(pos, gamma, sat, blur, arriba=0.0, abajo=0.0):
    alto = 1 - arriba - abajo
    base = f"crop=ih*{alto}*9/16:ih*{alto}:(iw-ih*{alto}*9/16)*{pos}:ih*{arriba},scale={ANCHO}:{ALTO}:flags=lanczos,fps=30"
    if blur:
        base += f",gblur=sigma={blur}"
    base += f",eq=gamma={gamma}:contrast=1.05:saturation={sat},format=gbrp"
    return (
        f"[0:v]{base},split[a][b];[b]lut3d=file='{LUT}':interp=tetrahedral[c];"
        f"[a][c]blend=all_mode=normal:all_opacity={MEZCLA_LUT},"
        "unsharp=7:7:0.7:5:5:0,vignette=PI/8,format=yuv420p,noise=alls=3:allf=t[v]"
    )


elegidos = sys.argv[1:] or list(PLANOS)
for nombre in elegidos:
    vid, entrada, dur, pos, gamma, sat, blur, *recorte = PLANOS[nombre]
    salida = os.path.join(SALIDA, f"{nombre}.mp4")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-threads", HILOS, "-ss", str(entrada), "-t", str(dur + 0.2), "-i", os.path.join(BROLL, f"m{vid}.mp4"), "-an",
         "-filter_complex", filtro(pos, gamma, sat, blur, *recorte), "-map", "[v]",
         "-c:v", "libx264", "-threads", HILOS, "-preset", "medium", "-crf", "15", "-g", "15",
         "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", salida],
        check=True,
    )
    print(nombre, flush=True)
with open(os.path.join(RAIZ, "fuente", "planos.json"), "w", encoding="utf8") as f:
    json.dump({k: v[0] for k, v in PLANOS.items()}, f, indent=2)
