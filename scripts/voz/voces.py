"""Locución con edge-tts (gratis, Dalia +9 %). Deja voz/<id>.mp3 y voz/lineas.json.

Espera estar en <proyecto>/fuente/ junto a guion.json y edge_fix.py.
"""
import asyncio
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edge_tts  # noqa: E402
import edge_fix  # noqa: E402,F401  (parche del host de edge-tts)

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOZ = [(g["id"], g["texto"], g["tts"]) for g in json.load(open(os.path.join(AQUI, "fuente", "guion.json"), encoding="utf-8"))]

OUT = os.path.join(AQUI, "voz")


def duracion(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta],
                       capture_output=True, text=True)
    return float(r.stdout)


async def gen(lid, texto, tts):
    mp3 = os.path.join(OUT, lid + ".mp3")
    marca = os.path.join(OUT, lid + ".txt")
    wj = os.path.join(OUT, lid + ".words.json")
    clave = tts or texto
    if os.path.exists(marca) and open(marca, encoding="utf-8").read() == clave and os.path.exists(wj):
        return {"id": lid, "text": texto, "duration": round(duracion(mp3), 3),
                "words": json.load(open(wj, encoding="utf-8"))}
    comm = edge_tts.Communicate(clave, "es-MX-DaliaNeural", rate="+9%", boundary="WordBoundary")
    words = []
    with open(mp3, "wb") as f:
        async for ch in comm.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                s = ch["offset"] / 1e7
                words.append({"text": ch["text"], "start": round(s, 3), "end": round(s + ch["duration"] / 1e7, 3)})
    json.dump(words, open(wj, "w", encoding="utf-8"), ensure_ascii=False)
    open(marca, "w", encoding="utf-8").write(clave)
    return {"id": lid, "text": texto, "duration": round(duracion(mp3), 3), "words": words}


async def main():
    os.makedirs(OUT, exist_ok=True)
    info = []
    for lid, texto, tts in VOZ:
        for intento in range(8):
            try:
                info.append(await gen(lid, texto, tts))
                await asyncio.sleep(2)
                break
            except Exception as e:  # el servicio gratis corta con 429 si se le pide seguido
                espera = 10 * (intento + 1)
                print(lid, "falló:", str(e)[:70], f"- reintento en {espera}s")
                await asyncio.sleep(espera)
        else:
            raise SystemExit("edge-tts no responde")
    json.dump(info, open(os.path.join(OUT, "lineas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i in info:
        print(i["id"], f'{i["duration"]:.2f}s | última palabra termina en {i["words"][-1]["end"]}')
    print("total voz:", round(sum(i["duration"] for i in info), 2))


asyncio.run(main())
