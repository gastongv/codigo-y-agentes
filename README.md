# Video con código

Recetas para producir videos publicitarios desde una PC, con HTML, ffmpeg y herramientas gratuitas, sin cámara ni programa de edición. Los videos de [GriftIA](https://griftia.com.ar) son el caso práctico.

**Documentación: <https://gastongv.github.io/video-con-codigo/>**

## Contenido

| Sección | Qué cubre |
| --- | --- |
| [Herramientas](docs/herramientas.md) | Qué se usa para imagen, audio y filmación |
| [Instalación en Windows](docs/instalacion-windows.md) | Puesta en marcha y tropiezos de Windows |
| [Flujo de trabajo](docs/flujo.md) | Del guion a la entrega |
| [Voz en off gratis](docs/recetas/voz.md) | edge-tts con tiempos por palabra |
| [Música, efectos y mezcla](docs/recetas/audio.md) | Mezcla con ffmpeg y master a -14 LUFS |
| [Subtítulos](docs/recetas/subtitulos.md) | Cortes, estilo y zonas seguras |
| [Animación 2D con HTML](docs/recetas/animacion-2d.md) | Generadores, personajes y GSAP sobre SVG |
| [Comercial 3D](docs/recetas/tres-d.md) | Receta de calidad con Eidoverse |
| [Filmación real de archivo](docs/recetas/filmacion-real.md) | Recorte vertical, color, marcas y HDR |
| [Producto en pantalla](docs/recetas/producto-en-pantalla.md) | Capturas reales de una aplicación |
| [Spot tipográfico](docs/recetas/tipografico.md) | Texto sincronizado con la música |
| [Explicadores](docs/recetas/explicadores.md) | Método de plan y reglas visuales |
| [Línea de tiempo para DaVinci](docs/recetas/davinci-otio.md) | Entrega editable en `.otio` |
| [Calidad y entrega](docs/recetas/entrega.md) | Formatos y versión liviana |
| [Cuidar la PC](docs/recetas/rendimiento.md) | Prioridad baja y límites de hilos |
| [Galería](docs/casos/index.md) | Los videos de GriftIA |
| [Criterios de guion y dirección](docs/casos/criterios.md) | Reglas de contenido |
| [Problemas conocidos](docs/problemas.md) | Síntomas y arreglos |
| [Scripts de ejemplo](scripts/README.md) | Código para copiar y adaptar |

## Ver el sitio en tu PC

```bash
pip install -r requirements.txt
mkdocs serve
```

## Publicar

El sitio se publica en GitHub Pages desde la rama `gh-pages`:

```bash
mkdocs gh-deploy
```

## Créditos

Música de Kevin MacLeod y personajes Toon Head de Johan Melin, ambos con licencia CC BY 4.0. El detalle está en [Créditos y licencias](docs/creditos.md). GriftIA y Griftin son marcas de Griftin.
