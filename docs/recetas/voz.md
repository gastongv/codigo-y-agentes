# Voz en off gratis

La locución sale de las voces neuronales de Microsoft por medio de [edge-tts](https://github.com/rany2/edge-tts). No cuesta nada y, además del audio, entrega el momento exacto en que empieza y termina cada palabra. Ese dato es el que sincroniza subtítulos y animaciones.

Script completo: [`scripts/voz/voces.py`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/voz/voces.py).

## El guion

Una lista de frases, cada una con su identificador:

```json
[
  {"id": "v1", "texto": "Tus clientes te escriben a cualquier hora.", "tts": null},
  {"id": "v5", "texto": "Con GriftIA, tu negocio responde al instante.",
               "tts": "Con Griftia, tu negocio responde al instante."}
]
```

`texto` es lo que se muestra en los subtítulos. `tts` es lo que se le manda a la voz cuando conviene escribirlo distinto para que lo pronuncie bien; si es `null`, se usa `texto`.

## Generar con tiempos por palabra

```python
comm = edge_tts.Communicate(texto, "es-MX-DaliaNeural", rate="+9%", boundary="WordBoundary")
palabras = []
with open("v1.mp3", "wb") as f:
    async for parte in comm.stream():
        if parte["type"] == "audio":
            f.write(parte["data"])
        elif parte["type"] == "WordBoundary":
            inicio = parte["offset"] / 1e7          # viene en décimas de microsegundo
            palabras.append({"text": parte["text"],
                             "start": round(inicio, 3),
                             "end": round(inicio + parte["duration"] / 1e7, 3)})
```

El script guarda un MP3 por frase y un `lineas.json` con la duración y las palabras de cada una. Lo que ya se generó queda en caché: solo se vuelve a pedir la frase que cambió.

## Voces y velocidad

| Voz | Uso |
| --- | --- |
| `es-MX-DaliaNeural` | Narradora principal. Fue la preferida por claridad y calidez. |
| `es-MX-JorgeNeural` | Voz masculina o de personaje. |
| `es-AR-ElenaNeural`, `es-AR-TomasNeural` | Alternativa con acento rioplatense. |

La velocidad se ajusta con `rate`. De +4 % a +9 % suena natural para publicidad; +12 % ya es apurado y sirve solo para cortos de humor. En un tramo acelerado a propósito se puede subir una frase suelta a +14 %.

## Error 403 al sintetizar

Desde octubre de 2026 el servidor que usa edge-tts por defecto rechaza la síntesis con `WSServerHandshakeError: 403`, incluso con la última versión publicada. La corrección está propuesta en el repositorio (PR 491) y se puede aplicar sin tocar el paquete, cambiando la dirección antes de crear el objeto:

```python
import edge_tts.communicate as _cm
from edge_tts.constants import TRUSTED_CLIENT_TOKEN as _T
_cm.WSS_URL = ("wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
               f"?Ocp-Apim-Subscription-Key={_T}")
```

Está en [`scripts/voz/edge_fix.py`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/voz/edge_fix.py): alcanza con importarlo. Cuando salga una versión corregida, se quita.

## Error 429

El servicio corta con 429 si se le piden muchas frases seguidas. El script espera dos segundos entre frases y reintenta con pausas crecientes (10 s, 20 s, 30 s…).

## Pronunciación

- **Nombres de marca.** Una marca con mayúsculas en el medio se puede leer deletreada o cortada. Escribirla en `tts` como palabra común ("Griftia" en lugar de "GriftIA") lo resuelve.
- **Siglas.** "IA" se lee "i-a", que es lo correcto en español.
- **Nombre pegado a otra palabra.** "Conocé GriftIA" no se entendía; "Conocé a Griftia." con una pausa más corta, sí.
- **Verificar.** Pasar el audio por un transcriptor y comparar con el guion detecta las palabras mal dichas sin tener que escuchar todo.

## Cuando la voz es una grabación real

Para usar la voz de una persona grabada con el celular en un evento:

1. Separar la voz del fondo con demucs (`htdemucs_ft`, en CPU).
2. Limpiar con ffmpeg: filtro pasa altos, reducción de ruido (`afftdn`), ecualización y compresor.
3. Transcribir con tiempos por palabra.
4. Elegir los tramos que se conservan y recortar las pausas.
5. Subtitular con el texto fiel a lo que la persona dice: el transcriptor se equivoca en palabras sueltas, así que el texto correcto se alinea con sus tiempos (por ejemplo con `difflib`) en lugar de usar la transcripción tal cual.

Usar solo palabras que la persona dijo de verdad. Clonar una voz para hacerle decir frases nuevas requiere el consentimiento expreso de esa persona.
