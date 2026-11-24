# Calidad y entrega

## Formato por defecto

Para redes, vertical: **1080×1920**, 30 cuadros por segundo, H.264, audio AAC a 48 kHz, con `+faststart` para que empiece a reproducirse antes de terminar de descargar.

Un 720p con la tasa de bits por defecto se rechazó por baja calidad. La calidad alta es el punto de partida, no un extra.

## Renderizar al doble y reducir

El texto y los bordes quedan más limpios si el maestro se renderiza al doble de tamaño y después se reduce con lanczos:

```bash
npx hyperframes@0.8.150 render --resolution portrait-4k --crf 12 -o renders/maestro.mp4
ffmpeg -i renders/maestro.mp4 -vf "scale=1080:1920:flags=lanczos" \
  -c:v libx264 -crf 16 -c:a copy -movflags +faststart final.mp4
```

Vale sobre todo para capturas de pantalla, texto chico y 3D. Para un spot de filmación real con textos grandes, renderizar directo a 1080×1920 con `--crf 12` alcanza.

## Calidad del codificador

| Uso | Valor |
| --- | --- |
| Maestro | CRF 12 a 16 |
| Entrega en alta | CRF 16 o 17, con tope de 12 Mbps |
| Clips intermedios | CRF 13 a 15 y `-g 15`, para que los cortes sean exactos |

Marcar siempre el color como bt709 (`-colorspace bt709 -color_primaries bt709 -color_trc bt709`): sin esa marca, algunos reproductores muestran los colores lavados.

## Versión liviana

Un maestro de 40 segundos puede pesar 100 MB. Para mandar por WhatsApp o subir a Instagram hace falta una versión de 5 a 30 MB que se vea igual de bien en un celular.

Codificación en dos pasadas con una tasa de bits fija: [`scripts/entrega/achicar.sh`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/entrega/achicar.sh).

```bash
achicar.sh entrada.mp4 salida.mp4 6000   # kbps de video
```

- **Dos pasadas:** la primera analiza, la segunda reparte los bits donde hacen falta.
- **Reducción de ruido suave** (`hqdn3d=1.2:1.2:4:4`): el grano fino es lo que más pesa y en un celular no se ve.
- Perfil High, nivel 4.1, un cuadro clave cada 60.

La tasa de bits depende de la imagen. Pesos reales de versiones livianas a 1080×1920:

| Video | Duración | Peso |
| --- | --- | --- |
| Explicador de formas planas | 37 s | 4 MB |
| Tipográfico | 16,5 s | 5 MB |
| Spot con filmación real | 38 s | 28 MB |

La animación plana comprime muchísimo; la filmación real necesita varias veces más bits para no mostrar bloques.

## Orden de entrega

Primero la versión liviana vertical, que es la que se va a mirar y reenviar. La versión 16:9 y los maestros, después.

## Versión horizontal

Un 16:9 no es el vertical recortado. La filmación se vuelve a hornear con otro recorte y la composición se reacomoda: textos al costado en lugar de arriba, el celular a un lado. Conviene que el generador reciba el formato como parámetro desde el principio.

## Audio

Objetivo de -14 LUFS con el pico cerca de -2 dB. La cadena está en [Música, efectos y mezcla](audio.md#master-para-redes).

## Revisión antes de entregar

- [ ] Cuadros del render final, no de la vista previa.
- [ ] Recortes mirados al 100 %.
- [ ] Texto dentro de las zonas seguras y sin tapar caras.
- [ ] La música se oye bajo la voz.
- [ ] Ninguna marca de terceros en la imagen.
- [ ] Subtítulos sincronizados y sin errores.
- [ ] Créditos de música y de personajes anotados para la publicación.
