"""Completa la línea de tiempo OTIO que escribió el MCP de DaVinci (planos + voz).

El autor sin conexión del MCP solo escribe una pista de video y una de audio. Acá se agregan, con la misma
estructura exacta de clips, la pista de música y las de efectos (los que se pisan van a pistas distintas).
Salida: entrega/<nombre>.otio
"""
import copy
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(RAIZ, "trabajo", "pistas-extra.json"), encoding="utf-8"))
o = json.load(open(os.path.join(RAIZ, "trabajo", "base-mcp.otio"), encoding="utf-8"))
FPS = m["fps"]
SALIDA = os.path.join(RAIZ, "entrega", m["nombre"] + ".otio")


def rt(v):
    return {"OTIO_SCHEMA": "RationalTime.1", "rate": FPS, "value": v}


def rango(ini, dur):
    return {"OTIO_SCHEMA": "TimeRange.1", "duration": rt(dur), "start_time": rt(ini)}


pistas = o["tracks"]["children"]
audio1 = next(t for t in pistas if t["kind"] == "Audio")
molde_clip = next(c for c in audio1["children"] if c["OTIO_SCHEMA"].startswith("Clip"))
molde_hueco = next(c for c in audio1["children"] if c["OTIO_SCHEMA"].startswith("Gap"))


def clip(ruta, dur):
    c = copy.deepcopy(molde_clip)
    c["name"] = os.path.basename(ruta)
    c["source_range"] = rango(0, dur)
    ref = c["media_references"]["DEFAULT_MEDIA"]
    ref["name"] = os.path.basename(ruta)
    ref["target_url"] = ruta
    ref["available_range"] = rango(0, dur)
    return c


def hueco(dur):
    g = copy.deepcopy(molde_hueco)
    g["source_range"] = rango(0, dur)
    return g


def pista(nombre, eventos):
    t = copy.deepcopy(audio1)
    t["name"] = nombre
    hijos, cur = [], 0
    for ruta, rec, dur in eventos:
        if rec > cur:
            hijos.append(hueco(rec - cur))
        hijos.append(clip(ruta, dur))
        cur = rec + dur
    t["children"] = hijos
    t["source_range"] = rango(0, cur)
    return t


pistas.append(pista("Audio 2", [(m["musica"]["ruta"], m["musica"]["rec"], m["musica"]["dur"])]))
# efectos: cada uno a la primera pista donde no pisa al anterior
carriles = []
for s in sorted(m["sfx"], key=lambda s: s["rec"]):
    dur = min(s["dur"], m["total"] - s["rec"])
    for c in carriles:
        if c[-1][1] + c[-1][2] <= s["rec"]:
            c.append((s["ruta"], s["rec"], dur))
            break
    else:
        carriles.append([(s["ruta"], s["rec"], dur)])
for i, c in enumerate(carriles):
    pistas.append(pista("Audio %d" % (3 + i), c))
o["tracks"]["source_range"] = rango(0, m["total"])
json.dump(o, open(SALIDA, "w", encoding="utf-8"), indent=1)
for t in pistas:
    n = len([c for c in t["children"] if c["OTIO_SCHEMA"].startswith("Clip")])
    print("%-8s %-6s clips: %2d  duración: %d cuadros" % (t["name"], t["kind"], n, t["source_range"]["duration"]["value"]))
print("salida:", SALIDA)
