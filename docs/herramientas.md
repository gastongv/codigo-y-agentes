# Herramientas

Todo el flujo corre en una PC con Windows, sin servicios pagos para la imagen. Cada herramienta cubre una parte; ninguna hace el video completo sola.

## Imagen

| Herramienta | Para qué se usa | Notas |
| --- | --- | --- |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Componer el video en HTML, CSS y GSAP y renderizarlo a MP4 | La CLI, el Studio y el render local son gratis. Solo es pago el catálogo de medios de HeyGen (voces, música), que acá no se usa. |
| [Eidoverse](https://github.com/SkyeShark/eidoverse-video) | Escenas 3D (Deno + WebGPU, Three.js) | Usa la placa de video. Ver [Comercial 3D](recetas/tres-d.md). |
| [FFmpeg](https://ffmpeg.org/) | Recortar y corregir filmación, mezclar audio, masterizar, comprimir | Es la herramienta que más se usa. Versión 9 instalada con winget. |
| [Playwright](https://playwright.dev/) | Capturar pantallas reales de una aplicación web a alta resolución | Ver [Producto en pantalla](recetas/producto-en-pantalla.md). |
| [DiceBear](https://www.dicebear.com/) | Personajes ilustrados (estilo Toon Head) como base de las caricaturas | Licencias CC0 y CC BY según el estilo. |
| [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve) | Retoque manual final, si alguien quiere editar a mano | La edición gratuita no acepta control externo: se le entrega un archivo `.otio`. Ver [Línea de tiempo para DaVinci](recetas/davinci-otio.md). |

## Audio

| Herramienta | Para qué se usa | Notas |
| --- | --- | --- |
| [edge-tts](https://github.com/rany2/edge-tts) | Voz en off con las voces neuronales de Microsoft | Gratis. Devuelve el tiempo de cada palabra, que después mueve los subtítulos y las animaciones. |
| [incompetech](https://incompetech.com/) | Música de Kevin MacLeod | CC BY 4.0: hay que acreditarla en la publicación. |
| Biblioteca de efectos de la skill `media-use` | Golpes, barridos, notificaciones, tecleo | Efectos de Pixabay incluidos con la skill. |
| [demucs](https://github.com/facebookresearch/demucs) | Separar la voz de una grabación con ruido o música | Modelo `htdemucs_ft`, en CPU. |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Transcribir con tiempos por palabra | Para subtitular una voz grabada. |
| [librosa](https://librosa.org/) | Detectar el tempo y los golpes de una canción | Para los spots tipográficos. |

## Filmación de archivo

| Fuente | Notas |
| --- | --- |
| [Mixkit](https://mixkit.co/free-stock-video/) | Sin clave. Muchos clips tienen versión 2160p, que permite recortar en vertical sin agrandar. |
| [Pexels](https://www.pexels.com/videos/) | Tiene filtro de orientación vertical. Algunos clips vienen en HDR y hay que convertirlos. |

## El agente que maneja todo

El trabajo se hace conversando con [Claude Code](https://claude.com/claude-code), que escribe los generadores, corre los comandos y revisa los cuadros. Sus *skills* son carpetas con instrucciones que le enseñan a usar cada herramienta:

- `hyperframes` y las de su familia (`hyperframes-core`, `hyperframes-animation`, `hyperframes-audio`, `hyperframes-cli`, `media-use`): vienen con el repositorio de HyperFrames.
- `ffmpeg-skill`: edición con FFmpeg.
- `ghost-editor` y `shorts`: edición de videos de una persona hablando a cámara y recorte de videos largos.
- [OpenMontage](https://github.com/OpenMontageInc/OpenMontage): flujos de producción completos.

Nada de esto es obligatorio: todos los comandos de esta documentación se pueden correr a mano.

## Otras herramientas probadas

| Herramienta | Resultado |
| --- | --- |
| [OpenCut](https://github.com/OpenCut-app/OpenCut) (variante classic) | Editor web parecido a CapCut. Sirve para editar a mano, no para generar en automático. |
| [Recordly](https://github.com/webadderallorg/Recordly) | Grabador de pantalla con zoom automático. Es manual; su estilo se recreó en HyperFrames para la demo de un panel. |
| Generadores de video por IA (Veo, Sora) | No se usaron por ser pagos. Un texto escrito para ellos sirve igual como guion de planos para una escena 3D. |
