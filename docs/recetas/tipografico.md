# Spot tipográfico

Un video de 15 segundos sin voz: una palabra o frase corta por golpe de la música, a pantalla completa, alternando colores de la marca. Es liviano (unos 5 MB), rápido de hacer y funciona sin sonido.

## Encontrar los golpes

[`scripts/audio/golpes.py`](https://github.com/gastongv/video-con-codigo/blob/main/scripts/audio/golpes.py) analiza la canción con librosa:

1. Detecta el tempo y el momento de cada golpe.
2. Busca la ventana de 17 segundos con más energía y más pareja que empiece justo en un golpe.
3. Guarda el tempo, el punto de inicio y la lista de golpes en `golpes.json`.

```python
tempo, golpes = librosa.beat.beat_track(y=y, sr=sr, units="time")
```

## Las tarjetas

El generador ([`scripts/hyperframes/tipografico-build.mjs`](https://github.com/gastongv/video-con-codigo/blob/main/scripts/hyperframes/tipografico-build.mjs)) define el video como una tabla: cada tarjeta entra en un golpe y sale en otro.

```js
// [id, golpe de entrada, golpe de salida, fondo, color de texto, contenido, tipo]
const T = [
  ["te",      0, 2, C.cian,  C.noche, "¿TE<br/>ESCRIBEN",   "letras"],
  ["3am",     2, 4, C.noche, "#fff",  "A LAS<br/>3 AM?",    "pal"],
  ["quien",   6, 8, C.cian,  C.noche, "¿QUIÉN<br/>RESPONDE?", "eco"],
  ["logo",    8, 12, C.gris, C.noche, "",                   "logo"],
  // …
];
```

Cambiar el guion es cambiar la tabla.

## Variedad

Si todas las tarjetas entran igual, cansa a los cinco segundos. Tipos de tarjeta usados:

| Tipo | Efecto |
| --- | --- |
| `letras` | Las letras entran de a una |
| `pal` | La frase entra entera y dura dos golpes |
| `eco` | Copias de la frase aparecen escalonadas arriba y abajo |
| `patron` | La palabra sobre un clip de video oscurecido, con renglones de texto repetido que se deslizan en sentidos opuestos |
| `golpe` | Una palabra que dura un solo golpe |
| `logo` | El logo, limpio y quieto, durante cuatro golpes |

## Reglas

- **Frases de dos o tres palabras.** Si no se lee en medio segundo, es larga.
- **El logo sin efectos.** Todo se mueve menos la marca.
- **Los golpes fuertes para las palabras clave.** El nombre del canal, el "24/7", el llamado a la acción.
- **Cierre fijo de unos dos segundos** con logo, lema y contacto: es el único cuadro que la gente alcanza a leer entero.
- El tamaño de cada texto se ajusta solo al ancho de la tarjeta (clase `ajusta`), así el guion se puede cambiar sin retocar tamaños.
