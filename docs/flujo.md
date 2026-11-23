# Flujo de trabajo

Un video sale de una cadena de pasos chicos. Cada paso deja un archivo que el siguiente lee, así que cualquier cambio se resuelve volviendo a correr desde ese punto y no editando a mano.

## Los pasos

| Paso | Qué se hace | Qué queda |
| --- | --- | --- |
| 1. Guion | Frases cortas, una idea por frase, con el plano que acompaña a cada una | `guion.json` o `GUION.md` |
| 2. Bocetos | Si hay personajes o un estilo nuevo, láminas con opciones para elegir | Imágenes de bocetos |
| 3. Voz | Se genera la locución y el tiempo de cada palabra | `voz/<id>.mp3` y `voz/lineas.json` |
| 4. Imagen | Un generador escribe la composición a partir del guion y de los tiempos de la voz | `index.html` |
| 5. Muestra | Cuadros sueltos o un clip corto para revisar antes del render | Capturas |
| 6. Render | HyperFrames (o el motor 3D) genera el video | `renders/*.mp4` |
| 7. Audio | Mezcla y master a volumen de redes | MP4 final |
| 8. Entrega | Versión liviana para compartir y, si hace falta, otra en 16:9 | MP4 liviano |

## Estructura de un proyecto

```
videos/mi-video/
├── fuente/          generadores y datos: lo único que se edita a mano
│   ├── guion.json
│   ├── voces.py
│   ├── build.mjs
│   └── hornear.py
├── voz/             locución y tiempos por palabra
├── broll/           filmación original descargada
├── assets/          clips ya recortados, música, efectos, fuentes, logos
├── index.html       composición generada: no se edita a mano
├── renders/         salidas del render
└── entrega/         el video final, los subtítulos y la línea de tiempo
```

## Generar, no editar

La composición (`index.html`) la escribe un script (`build.mjs`) y nunca se toca a mano. Tiene tres ventajas:

- **La voz manda.** El generador lee los tiempos por palabra y ubica cada animación en la palabra que le corresponde. Si cambia una frase, se regenera la voz y todo se vuelve a acomodar.
- **Las variantes salen casi gratis.** Tres cortos con la misma estructura comparten un módulo común y cada uno aporta solo sus textos. Una versión de Halloween y otra sin Halloween del mismo corto se diferencian en una capa de decoración.
- **Se puede rehacer.** Con el guion y el generador se reconstruye el video entero.

!!! warning "El orden importa"
    Cualquier paso que modifica `index.html` después del generador (por ejemplo, el ajuste de la música bajo la voz) se pierde al volver a generar. Hay que correrlo de nuevo cada vez.

## Mostrar antes de armar

Dos hábitos que ahorran más tiempo que cualquier optimización:

- **Bocetos antes de construir personajes.** Un estilo de personaje rechazado después de animarlo es un día perdido; rechazado en una lámina de bocetos, son minutos.
- **Muestra corta antes del render grande.** Un render 4K tarda diez minutos o más y ocupa la PC. Después de un cambio visual, primero van algunos cuadros clave o un clip breve en baja resolución, y el render completo recién con el visto bueno.

## Revisar el resultado

- Mirar cuadros del **render final**, no solo las capturas de la vista previa: hay fallas que aparecen únicamente en el render (ver [HDR](recetas/filmacion-real.md#clips-en-hdr)).
- Revisar los recortes al 100 % de tamaño.
- Escuchar que la música se oiga en los tramos con voz.
- Leer cada frase contra lo que se ve: el plano tiene que mostrar lo que la frase dice.
