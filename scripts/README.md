# Scripts de ejemplo

Son los scripts tal como se usaron en videos reales, con cambios mínimos. No son una biblioteca: cada uno espera la estructura de carpetas de un proyecto (`fuente/`, `voz/`, `broll/`, `assets/`, `trabajo/`, `entrega/`) y tiene valores propios del video para el que se escribió (planos, tiempos, música). Sirven para copiar y adaptar.

| Carpeta | Script | Qué hace | Receta |
| --- | --- | --- | --- |
| `voz/` | `voces.py` | Locución con edge-tts, tiempos por palabra, caché y reintentos | [Voz en off gratis](https://gastongv.github.io/codigo-y-agentes/recetas/voz/) |
| `voz/` | `edge_fix.py` | Parche para el error 403 de edge-tts | Ídem |
| `voz/` | `guion.json` | Ejemplo de guion | Ídem |
| `audio/` | `mezcla.py` | Mezcla de voz, música y efectos con un solo comando de ffmpeg | [Música, efectos y mezcla](https://gastongv.github.io/codigo-y-agentes/recetas/audio/) |
| `audio/` | `master.sh` | Lleva el audio a -14 LUFS sin recomprimir la imagen | Ídem |
| `audio/` | `golpes.py` | Tempo y golpes de una canción | [Spot tipográfico](https://gastongv.github.io/codigo-y-agentes/recetas/tipografico/) |
| `hyperframes/` | `tipografico-build.mjs`, `golpes.json` | Generador completo de un spot tipográfico | Ídem |
| `filmacion/` | `hornear.py` | Recorte vertical y color vivo de clips de archivo | [Filmación real de archivo](https://gastongv.github.io/codigo-y-agentes/recetas/filmacion-real/) |
| `filmacion/` | `hornear_cine.py` | Lo mismo con aspecto de película | Ídem |
| `filmacion/` | `hoja_marcas.py` | Hojas de cuadros para buscar marcas de terceros | Ídem |
| `davinci/` | `armar.py` | Corta el render en planos, separa los audios, escribe el `.srt` y mezcla el video final | [Línea de tiempo para DaVinci](https://gastongv.github.io/codigo-y-agentes/recetas/davinci-otio/) |
| `davinci/` | `otio_final.py` | Agrega las pistas de música y efectos al `.otio` | Ídem |
| `entrega/` | `liviano.sh`, `achicar.sh` | Versión liviana en dos pasadas | [Calidad y entrega](https://gastongv.github.io/codigo-y-agentes/recetas/entrega/) |
| `windows/` | `bajo.ps1` | Corre un comando con prioridad baja | [Cuidar la PC](https://gastongv.github.io/codigo-y-agentes/recetas/rendimiento/) |

Los `.sh` están escritos para Git Bash en Windows: la primera pasada de ffmpeg descarta la salida en `NUL`. En Linux o macOS, cambiarlo por `/dev/null`.
