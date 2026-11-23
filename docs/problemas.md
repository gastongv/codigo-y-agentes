# Problemas conocidos

Lista rápida de síntomas y arreglos. El detalle de cada uno está en la receta enlazada.

## Voz

| Síntoma | Arreglo |
| --- | --- |
| `WSServerHandshakeError: 403` en edge-tts | Cambiar la dirección del servicio antes de sintetizar. [Voz](recetas/voz.md#error-403-al-sintetizar) |
| Error 429 al generar varias frases | Pausa entre frases y reintentos con espera creciente |
| La marca se pronuncia mal | Escribirla distinto solo para la voz (campo `tts`) |
| "Python was not found" al llamar `python3` | [Copia de `python.exe` como `python3.exe`](instalacion-windows.md#python3-apunta-a-la-microsoft-store) |

## Audio

| Síntoma | Arreglo |
| --- | --- |
| La música no se oye | Ajuste bajo la voz con `--strength 0.3` y base entre 0,5 y 0,6. [Audio](recetas/audio.md#que-la-musica-se-oiga) |
| La música desaparece después de regenerar | El generador reescribe `index.html`: volver a correr el ajuste |
| El video suena bajo en redes | Master a -14 LUFS. [Audio](recetas/audio.md#master-para-redes) |
| Pico por encima de cero después de normalizar | No usar `loudnorm` de una pasada: ganancia medida y limitador con sobremuestreo |
| El render falla con "unknown effect type: truepeak" | Quitar ese efecto de la cadena (HyperFrames 0.8.145) |
| Un barrido crece debajo de la voz | Usar solo el último segundo del archivo |

## Imagen

| Síntoma | Arreglo |
| --- | --- |
| Render lentísimo, colores lavados y textos que faltan | Un clip en HDR. Marcar todo bt709 al hornear y renderizar con `--sdr`. [Filmación real](recetas/filmacion-real.md#clips-en-hdr) |
| Un elemento SVG se desplaza al animarse | Poner `svgOrigin` también en los valores iniciales. [Animación 2D](recetas/animacion-2d.md#gsap-sobre-svg) |
| Una tacha pierde su inclinación | `scaleX` pisa el `rotate` del CSS: llevar la rotación a la animación |
| Queda un punto antes de que se dibuje un trazo | Arrancar el trazo con opacidad 0 |
| El "¿" pisa el renglón de abajo | Subirlo con `top: -0.17em`. [Subtítulos](recetas/subtitulos.md#detalle-tipografico) |
| Texto 3D con contornos rotos | Cambiar de fuente. [Comercial 3D](recetas/tres-d.md#texto-en-3d) |
| Halos alrededor del texto en 3D | Subir el umbral del resplandor a 1,4 |
| Se mueve el grupo en lugar del objeto | `add()` devuelve el padre |
| "expected ArrayBuffer" al crear una textura | Usar un canvas del documento |
| Las luces se ven en escalones | La cadena de grano posteriza: usar la tabla de color y grano propio |
| Una captura sale con un recorrido guiado encima | Esperarlo y saltearlo en el script. [Producto en pantalla](recetas/producto-en-pantalla.md#guias-de-primera-vez) |

## Windows

| Síntoma | Arreglo |
| --- | --- |
| Git Bash no encuentra `ffmpeg` | Agregar la carpeta de enlaces de winget al `PATH` |
| Un valor llega con `\r` y el comando falla | `core.autocrlf false` en ese repositorio |
| Una ruta `/x` se convierte en `C:/Program Files/Git/x` | Conversión de rutas de Git Bash: evitar argumentos que empiecen con `/` |
| El JSON de variables llega sin comillas | `--variables-file` |
| La base de datos se cae sola | WSL se apagó: mantener una sesión abierta |
| Un proceso a prioridad mínima no avanza | Usar `BelowNormal`, no `Idle`. [Cuidar la PC](recetas/rendimiento.md#prioridad-baja-en-windows) |

## DaVinci Resolve

| Síntoma | Arreglo |
| --- | --- |
| Los scripts externos devuelven vacío | Es la edición gratuita. Entregar un `.otio`. [DaVinci](recetas/davinci-otio.md) |
| El menú de scripts no lista archivos `.py` | Desde la versión 21.1 de la edición gratuita, solo Lua |
| Los títulos importados quedan vacíos | Llevar el texto como `.srt` o compuesto en la imagen |
