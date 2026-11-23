# Animación 2D con HTML

Las caricaturas, los paneles y los textos animados son páginas HTML con SVG y CSS, animadas con GSAP y renderizadas con [HyperFrames](https://github.com/heygen-com/hyperframes). La documentación de HyperFrames explica el formato de la composición; acá va lo que se aprendió usándolo.

## Un generador por video

El generador (`fuente/build.mjs`) es un script de Node que escribe `index.html`. Recibe el guion, los tiempos de la voz y los datos de cada escena, y devuelve la composición completa.

```bash
node fuente/build.mjs
npx hyperframes@0.8.150 check
npx hyperframes@0.8.150 render --resolution portrait -o renders/video.mp4
```

Ejemplo real, corto y completo: [`scripts/hyperframes/tipografico-build.mjs`](https://github.com/gastongv/video-con-codigo/blob/main/scripts/hyperframes/tipografico-build.mjs).

Para una serie de videos parecidos, un módulo común exporta las piezas (personaje, chat, decoración, cierre con logo, subtítulos, audio) y cada video tiene un archivo corto con sus textos y su elenco.

## Personajes

### Elegir el estilo con bocetos

Antes de dibujar, una lámina con opciones. [DiceBear](https://www.dicebear.com/) genera personajes en varios estilos con licencias libres; con seis estilos lado a lado, elegir lleva un minuto.

El estilo que quedó fue **Toon Head** (de Johan Melin, CC BY 4.0), que trae cabeza y hombros. Para tener cuerpo completo se le dibujó torso, brazos y piernas con el mismo trazo.

### Armarlos por partes

Cada personaje es un SVG con grupos identificados, para animar cada parte por separado:

```
cabeza   ojos   cejas   boca   brazo-izq   brazo-der   cuerpo   pies
```

Las expresiones son combinaciones de ojos, cejas y boca. Se apilan todas las variantes y se muestra una por vez.

### Brazos sin articulaciones a la vista

Los brazos hechos con rectángulos superpuestos en hombro y codo se ven como un muñeco articulado. La versión que funcionó dibuja **cada brazo como un solo trazo curvo** (una curva cuadrática hombro, codo, mano) con contorno, y recalcula ese trazo en cada cuadro. Piernas y cadera van como una sola pieza.

### Reglas de estilo que funcionaron

- Formas planas y redondeadas; nada en punta.
- Ojos grandes y geométricos; cejas simples; boca que cambia de forma al hablar.
- Exagerar el rasgo que identifica a cada personaje (pelo, ropa, un accesorio).
- Fondos claros y con aire, para que el personaje resalte.
- Todo en movimiento: parpadeo, rebote suave, boca sincronizada. Los cuadros quietos se notan.

Se puede tomar como referencia el lenguaje visual de una marca conocida, pero nunca sus personajes.

## GSAP sobre SVG

!!! warning "Cosas que rompen la animación"
    - En un `fromTo` sobre un elemento SVG, el `svgOrigin` tiene que estar **también en los valores iniciales**. Si está solo en los finales, el elemento se desplaza.
    - Para piezas sueltas, usar `transformOrigin: "50% 50%"`.
    - Animar `scaleX` pisa un `rotate` puesto por CSS. La rotación tiene que ir dentro de la misma animación (`rotation` en el `fromTo`).
    - Un brazo con el codo anidado no se puede rotar con `rotation` de GSAP. Se anima un objeto intermedio y en cada actualización se reescribe el atributo `transform="rotate(ángulo cx cy)"`.
    - Un trazo SVG con `stroke-linecap: round` y `stroke-dashoffset` igual a su largo deja un punto visible antes de dibujarse. El trazo tiene que arrancar con opacidad 0.

## Texto y logos

- El logo se usa desde su archivo SVG, con el texto convertido a curvas. No se redibuja ni se recolorea.
- Para convertir texto a curvas con opentype.js: `toPathData()` puede escribir `NaN`. Conviene serializar los comandos del trazo con una función propia.

## Recursos para la web a partir del mismo proyecto

Una animación en bucle con fondo transparente (una mascota para un sitio web, por ejemplo) sale de la misma composición:

1. Renderizar como secuencia de PNG: `render --format png-sequence`.
2. Recortar los márgenes vacíos.
3. Codificar con ffmpeg desde los cuadros sin pérdida:
    - WebM con VP9 y canal alfa (unos 0,6 a 0,85 MB a 720 px).
    - WebP animado para Safari y iPhone (unos 2 MB a 15 cuadros por segundo).
    - Un PNG fijo como imagen de espera.

## Detalles de la CLI

- `lint` solo acepta una carpeta de proyecto. Para validar una composición suelta hay que copiarla a una carpeta temporal con el nombre `index.html`.
- El efecto `truepeak` en la cadena de audio hacía fallar el render en la versión 0.8.145.
- Para ver la composición en un navegador automatizado, servir la carpeta por HTTP (`python -m http.server`); las direcciones `file://` suelen estar bloqueadas.
