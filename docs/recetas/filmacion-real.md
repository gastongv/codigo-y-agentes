# Filmación real de archivo

Para los spots con imagen real se usa filmación libre de Mixkit y Pexels. Cada clip se prepara una sola vez ("hornear"): recorte vertical, color y duración exacta. La composición después trabaja con archivos livianos y parejos.

## Conseguir los clips

**Mixkit** no pide clave. Las direcciones siguen un patrón fijo:

| Qué | Dirección |
| --- | --- |
| Búsqueda por tema | `https://mixkit.co/free-stock-video/<tema>/` |
| Miniatura | `https://assets.mixkit.co/videos/<id>/<id>-thumb-720-0.jpg` |
| Archivo 4K | `https://assets.mixkit.co/videos/<id>/<id>-2160.mp4` |

No todos los clips tienen versión 2160p. Para saberlo sin descargar, alcanza con un pedido `HEAD` al archivo. La página de búsqueda limita la cantidad de pedidos (responde 429): espaciarlos.

**Pexels** permite filtrar por orientación: `https://www.pexels.com/search/videos/<tema>/?orientation=portrait`. La descarga está en `https://www.pexels.com/download/video/<id>/`.

Revisar la licencia en la página de cada clip antes de usarlo.

## Por qué 4K

Un clip horizontal de 3840×2160 recortado en vertical da 1216×2160: más que los 1080×1920 que hacen falta. Sobra detalle para un empuje de cámara y para recortar bordes con carteles. Con un original de 1080p, el recorte vertical obliga a agrandar y se nota.

## Hornear

Versión luminosa, de color vivo: [`scripts/filmacion/hornear.py`](https://github.com/gastongv/video-con-codigo/blob/main/scripts/filmacion/hornear.py).

```text
crop=ih*9/16:ih:(iw-ih*9/16)*POS:0,
scale=1080:1920:flags=lanczos,
setpts=N/30/TB,
eq=gamma=G:contrast=1.06:saturation=S,
unsharp=5:5:0.5:5:5:0,
format=yuv420p,
setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709
```

- `POS` (de 0 a 1) elige qué parte del ancho queda en el recorte.
- `gamma` y `saturation` se ajustan **por plano**: cada clip viene con otra exposición.
- `setpts=N/30/TB` toma un cuadro de origen por cuadro de salida. Un original de 24 o 25 cuadros queda un 20 a 25 % más rápido, sin cuadros repetidos ni saltos.
- Cada plano se hornea con unos cuadros de más, para que la composición tenga margen en los cortes.

## Aspecto de cine sin oscurecer

Versión con aspecto de película: [`scripts/filmacion/hornear_cine.py`](https://github.com/gastongv/video-con-codigo/blob/main/scripts/filmacion/hornear_cine.py).

La primera versión de este estilo quedó oscura. La causa fueron tres cosas juntas: la tabla de color (LUT) aplicada entera, el brillo en negativo y una viñeta fuerte. Lo que quedó:

| Ajuste | Valor |
| --- | --- |
| LUT de película (Vision3 500T) | Mezclada al **40 %** con la imagen original |
| Gamma | Por plano, entre 1,0 y 1,45 |
| Contraste | 1,05 |
| Nitidez | `unsharp` suave |
| Viñeta | `PI/8` |
| Grano | `noise=alls=3` |

Por defecto conviene elegir planos con luz de día o de atardecer.

## Buscar marcas

Los clips de archivo traen logos: monitores, zapatillas, carteles de comercios, emblemas en paredes. En una publicidad no pueden aparecer marcas de terceros.

- Buscar en el **original al 100 %** y a lo largo de **todo el plano**. En las miniaturas chicas no se ven.
- [`scripts/filmacion/hoja_marcas.py`](https://github.com/gastongv/video-con-codigo/blob/main/scripts/filmacion/hoja_marcas.py) arma hojas con tres cuadros de cada plano (principio, medio y final) con el mismo recorte vertical y la imagen aclarada.
- La mayoría se resuelve **recortando**: el 4K da margen para sacar el borde donde está el logo sin perder nitidez.
- Si no se puede recortar, se cambia el plano.

## Clips en HDR

Varios clips de Pexels vienen marcados como HDR (HLG, bt2020). Con uno solo en la composición, HyperFrames pasa todo el render a HDR: tarda más de diez minutos, lava los colores y **se pierden los textos** de buena parte del video. En las capturas de vista previa no se nota.

Dos medidas, las dos necesarias:

1. Al hornear, marcar todo como bt709 con `setparams` (está en el filtro de arriba).
2. Renderizar con `--sdr`.

Y mirar siempre cuadros del render final.

## Elegir el plano

- **Cada plano muestra lo que dice la frase.** Si la voz dice "el domingo", se ve un domingo. Revisar cuadro por cuadro.
- Para "tu equipo", personas atendiendo en un negocio real. Las imágenes de gente con auriculares frente a computadoras se leen como un centro de llamadas.
- Descartar planos donde lo importante no se ve (un brazo suelto, una cara seria para una frase alegre).

## Servicios y claves

Las claves de API de Pexels pueden dejar de funcionar sin aviso. Conviene que el flujo no dependa de una: con la búsqueda web y la descarga directa alcanza.
