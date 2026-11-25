# Cortos

Cada corto explica en unos 20 segundos cómo se arma una cosa: qué se hace, con qué herramienta, por qué esa y dónde sirve. Acá está cada uno con su explicación completa.

Los cortos salen en TikTok, en [@codigoyagentes](https://www.tiktok.com/@codigoyagentes), los martes y los viernes.

## 01 · Subtítulos que se sincronizan solos

<div class="galeria" markdown>

<figure markdown>
<video controls preload="none" poster="../media/cuadros/corto-01.jpg" src="../media/video/corto-01.mp4"></video>
</figure>

</div>

**Qué se hace.** Subtítulos que marcan cada palabra en el momento en que se dice, sin escribir un solo tiempo a mano.

**Con qué.** [edge-tts](https://github.com/rany2/edge-tts), una herramienta gratuita que genera la voz y además devuelve el instante en que empieza y termina cada palabra.

**Por qué.** Con esos tiempos, un programa arma los grupos de palabras y los ubica solo. Si cambia una frase, se regenera la voz y los subtítulos se acomodan.

**Dónde sirve.** En cualquier video narrado: reels, tutoriales, anuncios.

**El paso a paso:** [Voz en off gratis](../recetas/voz.md) y [Subtítulos](../recetas/subtitulos.md). El script completo está en [`scripts/voz/voces.py`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/voz/voces.py).

## Próximos

| Corto | Tema | Sale |
| --- | --- | --- |
| 02 | Una palabra por golpe | 27 de noviembre |
| 03 | De horizontal a vertical | 1 de diciembre |
| 04 | Tu aplicación en un video | 4 de diciembre |
| 05 | Que tu video no suene bajo | 8 de diciembre |
| 06 | Caricaturas por partes | 11 de diciembre |
| 07 | La música baja sola | 15 de diciembre |
| 08 | Un comercial 3D con código | 18 de diciembre |

Música de los cortos: "Digital Lemonade" de Kevin MacLeod (incompetech.com), licencia CC BY 4.0.