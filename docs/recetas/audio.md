# Música, efectos y mezcla

## Música

Las pistas son de Kevin MacLeod ([incompetech.com](https://incompetech.com/)), con licencia CC BY 4.0. Se pueden usar en publicidad, pero **hay que acreditarlas** en el texto de la publicación.

| Pista | Dónde funcionó |
| --- | --- |
| Inspired | Comerciales sobrios, cierres, amaneceres |
| Digital Lemonade | Demos de producto, spots de ritmo medio |
| Tech Live | Tipográficos (123 BPM) y escenas nocturnas |
| Rising Tide | Reel corporativo |
| Monkeys Spinning Monkeys, Fluffing a Duck, Happy Bee, Carefree | Caricaturas y cortos de humor |
| Sneaky Snitch, Scheming Weasel, In the Hall of the Mountain King | Cortos de Halloween |

No hace falta usar la canción desde el principio. Muchas tienen una introducción larga: conviene buscar el tramo con más energía y arrancar ahí.

## Que la música se oiga

El error más común es dejar la música tan abajo que desaparece. Pasó con la base a 0,42 de volumen y un ajuste automático bajo la voz con intensidad 0,8: como la narración ocupaba casi todo el video, la música quedaba 19 dB abajo, o sea muda.

Lo que funciona en videos con voz casi continua:

- Volumen de la base entre **0,5 y 0,6**.
- Ajuste bajo la voz **suave**: que baje unos 6 o 7 dB mientras se habla, no más.

Con HyperFrames, el ajuste lo hace el script `carve.mjs` de la skill `hyperframes-audio`:

```bash
node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs \
  --comp index.html --bed bgm --strength 0.3
```

Si el proyecto no tiene `node_modules`, se le indica otro que sí con `--core ../otro-proyecto`. El valor por defecto de `--strength` es 0,8: demasiado para este tipo de video.

!!! note "El volumen de cada archivo es distinto"
    "Inspired" viene grabada muy alta: a 0,5 tapaba la voz y hubo que bajarla a 0,24. Los números de arriba son un punto de partida; siempre hay que escuchar.

## Mezcla solo con ffmpeg

Cuando el video no sale de HyperFrames (por ejemplo, una escena 3D), la mezcla se hace con un único comando de ffmpeg que arma un script de Python. Ejemplo completo: [`scripts/audio/mezcla.py`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/audio/mezcla.py).

La cadena:

1. Cada frase de voz se ubica en su momento con `adelay`.
2. La música va 10 dB por debajo de la voz, con fundido de entrada y de salida.
3. Un compresor con cadena lateral (`sidechaincompress`) la baja unos 6 dB más mientras se habla.
4. Los efectos se ubican con `adelay` y su volumen propio.
5. Todo pasa por un limitador.

```text
[voz]asplit=2[voz1][key];
[mus][key]sidechaincompress=threshold=0.03:ratio=3:attack=30:release=450:makeup=1[musd];
[voz1][musd][fx]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.89:level=disabled[out]
```

`normalize=0` en `amix` es importante: sin eso, ffmpeg baja el volumen de cada entrada según cuántas haya.

## Efectos atados a las palabras

Los efectos no se ubican por segundo fijo sino por palabra. Con los tiempos de la voz se calcula cuándo se dice cada cosa:

```python
W = lambda linea, k: INICIO[linea] + LINEAS[linea]["words"][k]["start"]
tAgenda = W("vo-05", 7)            # la palabra "agenda"
EFECTOS = [("chime", tAgenda - 0.1, 0.3)]
```

Si cambia la voz, los efectos se reacomodan solos.

## Reglas para los golpes

- **Nunca un golpe encima del nombre de la marca.** Va en el corte, antes de que la voz lo diga, y bajo (0,26 de volumen).
- **Los barridos largos se recortan.** Un `riser` de 10 segundos entero crece debajo de la voz; se usa solo el último segundo.
- **Una voz de personaje que cae sobre un golpe necesita más volumen:** +5 dB respecto de la narradora.

## Master para redes

El mezclador de HyperFrames baja toda la mezcla para no pasarse de pico y el resultado puede quedar en -18 LUFS, bajo para Reels. El objetivo es **-14 LUFS**.

No usar `loudnorm` de una sola pasada: deja el pico real en -0,3 dB o directamente por encima de cero. La cadena que dio resultado es medir, aplicar la ganancia que falta y limitar con sobremuestreo:

```bash
ffmpeg -i entrada.mp4 -c:v copy \
  -af "volume=4.2dB,aresample=192000,alimiter=limit=0.78:level=false,aresample=48000" \
  -c:a aac -b:a 160k -movflags +faststart salida.mp4
```

El sobremuestreo a 192 kHz hace que el limitador vea los picos reales entre muestras. Con `limit=0.78` el pico queda cerca de -2 dB.

[`scripts/audio/master.sh`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/audio/master.sh) mide el volumen del archivo, calcula la ganancia y aplica esa cadena sin recomprimir la imagen.
