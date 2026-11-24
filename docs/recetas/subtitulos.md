# Subtítulos

Todos los videos llevan subtítulos: la mayoría se ve sin sonido.

## De dónde salen

De los tiempos por palabra de la voz (ver [Voz en off gratis](voz.md)). El generador arma los grupos de palabras y los ubica en la línea de tiempo; nadie escribe tiempos a mano.

## Dónde cortar

- Una idea por línea.
- Cortar **después de cada coma o punto**. Los cortes por cantidad de palabras parten las frases en lugares raros.
- Cuando un corte automático queda mal, se corrige en una tabla de excepciones dentro del generador, no en la composición.

```python
for i, palabra in enumerate(palabras):
    grupo.append(i)
    if palabra.endswith((",", ".")) or i == len(palabras) - 1:
        inicio, fin = tiempos[grupo[0]]["start"], tiempos[grupo[-1]]["end"]
        subtitulos.append((" ".join(palabras[j] for j in grupo), inicio, fin + 0.1))
        grupo = []
```

## Estilo

- Píldora oscura detrás del texto (azul noche), para que se lea sobre cualquier imagen.
- La palabra que se está diciendo va resaltada en el color de acento.
- Texto blanco sobre fondos claros o cálidos no se lee: ahí la píldora es obligatoria.
- En los rótulos sobre filmación real, una sombra radial suave detrás del título funciona mejor que un óvalo marcado.

## Zonas seguras en vertical

Instagram y TikTok tapan partes de la pantalla con su interfaz. En 1080×1920:

| Elemento | Posición |
| --- | --- |
| Todo el texto | Entre los 168 y los 1330 px de altura |
| Subtítulos | Cerca del 81 % de la altura en videos sin interfaz superpuesta; más arriba si el video se pauta |
| Título chico y dirección web | Cerca del 11,5 % |
| Borde derecho | Nada importante: ahí van los botones |

Revisar además que los títulos no tapen caras.

## Los textos grandes también subtitulan

En un spot rápido, los textos animados grandes que repiten la locución hacen de subtítulos. Igual conviene entregar el archivo `.srt` aparte.

## Archivo `.srt`

Para quien edite después, o para subirlo como subtítulos de la plataforma:

```python
def tc(t):
    ms = int(round(t * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)

with open("subtitulos.srt", "w", encoding="utf-8") as f:
    for i, (texto, a, b) in enumerate(subtitulos, 1):
        f.write("%d\n%s --> %s\n%s\n\n" % (i, tc(a), tc(b), texto))
```

El fin de cada subtítulo se recorta para que no pise el comienzo del siguiente. Está resuelto en [`scripts/davinci/armar.py`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/davinci/armar.py).

## Detalle tipográfico

En algunas fuentes (Spartan, por ejemplo) el signo "¿" cuelga por debajo de la línea y pisa el renglón de abajo en textos grandes. Se envuelve en un `span` con `position: relative; top: -0.17em` y se usa un interlineado de 1,12.
