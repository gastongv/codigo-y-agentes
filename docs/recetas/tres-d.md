# Comercial 3D

Las escenas 3D se hacen con [Eidoverse](https://github.com/SkyeShark/eidoverse-video), un motor sobre Deno, WebGPU y Three.js. La escena es un archivo `scene.js` y el audio se mezcla aparte con ffmpeg.

!!! note "Usa la placa de video"
    A diferencia del resto del flujo, el render 3D ocupa la GPU. Un comercial de 35 segundos a 2160×3840 tarda unos 2 minutos.

## La escena como función del tiempo

Escribir `animate` como una función pura del tiempo `t` (sin estado acumulado entre cuadros) permite saltar a cualquier instante para revisar un plano sin renderizar lo anterior:

```bash
python eido.py render work/mi_video/scene_preview.json --at 12.5 --jump
```

Conviene tener dos configuraciones: una de vista previa a 1080×1920 y la definitiva al doble.

## Receta de calidad

La primera versión salió a 1280×720 con los valores por defecto y se rechazó por baja calidad. Las causas y los arreglos:

| Problema | Causa | Arreglo |
| --- | --- | --- |
| Imagen lavada y con bloques | El codificador del motor usa 8 Mbps con perfil rápido | `RENDER_CQ=16` |
| Texto blando | El suavizado de bordes (FXAA) del realce automático | Renderizar al doble (2160×3840) y bajar con lanczos |
| Blancos quemados y halos en el texto | El resplandor por defecto arranca en 0,85 | `globalThis._bloomParams = {threshold: 1.4}` y materiales emisivos con intensidad mayor a 1,4 |
| Aspecto plástico barato | Luz plana | Barniz (`clearcoat`), sombra de 4096 en la luz principal, contraluz y un entorno de estudio procedural como `environmentNode` |
| Colores de marca corridos | El mapeo de tonos | `NeutralToneMapping`; las capas 2D se componen antes del mapeo de tonos |

Entrega:

```bash
RENDER_CQ=16 python eido.py render work/mi_video/scene.json
ffmpeg -i maestro.mp4 -i mezcla.wav -vf "scale=1080:1920:flags=lanczos" \
  -c:v libx264 -crf 16 -c:a aac -movflags +faststart final.mp4
```

## Texto en 3D

- No todas las fuentes sobreviven a la extrusión. Con Spartan Black los números salían con los contornos rotos; Archivo Black funcionó bien.
- Algunas fuentes de título (Bungee) no tienen minúsculas: verificarlo si la marca las usa.
- Un logo plano se convierte en objeto 3D extruyendo su SVG. El texto del logo conviene ponerlo como imagen recortada del PNG oficial, no recrearlo.
- El texto en texturas de canvas necesita resolución de sobra.

## Sin personaje

Cuando un personaje 3D queda rígido o robótico, la historia se puede contar con los objetos: el cartel del consultorio con el neón "CERRADO", el celular con el chat, la agenda que se va llenando. La persona aparece por su nombre en el cartel y en la conversación.

## Tiempos compartidos con el audio

Los momentos en que arranca cada frase están en dos lugares: `scene.js` (para la imagen) y `mezcla.py` (para el audio). Si se cambia uno, hay que cambiar el otro. Lo mismo con `lines.json`: si se regenera la voz, se copia de nuevo a la carpeta de la escena.

La boca de un personaje se puede animar con la envolvente de volumen de la voz, exportada a un JSON.

## Problemas de Three.js que costaron tiempo

- `grupo.add(malla).position.set(...)` mueve **el grupo**, no la malla: `add` devuelve el padre.
- Las texturas creadas con el `createCanvas` de `@napi-rs/canvas` fallan al subirse a la GPU ("expected ArrayBuffer"). Usar `document.createElement('canvas')`.
- Si algún objeto hace `lookAt(camera.position)`, la cámara tiene que calcularse al principio de `animate`.
- Para apoyar un objeto inclinado sobre una mesa, cambiar el orden de rotación: `rotation.order = 'YXZ'`.
- Con `--jump`, las capas 2D pueden mostrar el contenido del cuadro pedido antes. En el render completo no pasa.
- Texto blanco sobre un fondo cálido no se lee: va con una píldora oscura detrás.
