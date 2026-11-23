# Producto en pantalla

Un comercial de un producto de software convence más con las pantallas reales que con un dibujo del panel. La receta: levantar la aplicación en un entorno propio, cargarle datos de demostración, capturarla a alta resolución y animar esas capturas.

## Entorno separado

- Una copia de la aplicación corriendo en **su propio puerto** y contra **su propia base de datos**. Nunca la base de desarrollo de todos los días ni la de producción.
- Servicios externos simulados (correo, modelos de IA, mensajería).
- Una cuenta creada solo para el video.

Las credenciales de esa cuenta van en variables de entorno o en un archivo que no se sube al repositorio.

## Datos de demostración

Un script de carga deja la aplicación como se quiere mostrar: un negocio con nombre creíble, conversaciones, turnos en la agenda.

- **Coherentes con el rubro.** En una peluquería se pregunta por turnos, precios y servicios; nadie pregunta si hacen envíos.
- **En el idioma y el trato del público.** Voseo y precios en pesos para Argentina; "ustedes" para Canarias.
- **Con fechas pensadas.** Si la historia transcurre un domingo, los mensajes tienen fecha de domingo. Conviene fijar la fecha de la historia en la configuración: si se calcula desde el día de hoy, las pantallas cambian cada vez que se regenera.
- **Respetando las reglas de la aplicación.** Si la agenda no admite turnos superpuestos, el script tampoco puede cargarlos.

!!! tip "Ventanas de tiempo"
    Algunas pantallas cambian según la antigüedad de los datos (por ejemplo, una conversación que ya no se puede responder pasadas 24 horas). Capturar el mismo día de la carga o volver a cargar antes de capturar.

## Captura con Playwright

Esquema del script de captura:

```js
const navegador = await chromium.launch();
const pagina = await navegador.newPage({
  viewport: { width: 430, height: 932 },   // tamaño de un celular
  deviceScaleFactor: 4,                    // 1720×3728 px reales
});
await pagina.goto(`${BASE}/conversaciones`);
await pagina.addStyleTag({ content: OCULTAR });
await pagina.screenshot({ path: "png/bandeja.png" });
```

| Pantalla | Tamaño | Densidad |
| --- | --- | --- |
| Vista de celular | 430×932 | 4 |
| Vista de escritorio | 1600×900 o 1600×1000 | 2 |

Con esa densidad, la cámara puede acercarse a un detalle sin que se pixele.

### Qué ocultar

Antes de capturar se inyecta una hoja de estilos que esconde lo que no es parte del producto que se muestra:

- Avisos de entorno de prueba.
- Avisos de plan, de pago o de configuración pendiente.
- Asistentes de ayuda flotantes.
- El indicador de desarrollo del framework.

### Guías de primera vez

La primera vez que entra una cuenta nueva suele aparecer un recorrido guiado. El script de captura tiene que esperarlo y saltearlo; si no, la captura sale con el recorrido encima.

### Posiciones de los elementos

Junto con cada PNG, el script guarda en un JSON la posición y el tamaño de los elementos que después se van a destacar (un botón, un mensaje, una tarjeta). El generador del video usa esas cajas para mover la cámara y el cursor sin medir nada a mano.

## Animar las capturas

- **Cámara:** empuje lento y acercamientos a la zona que nombra la voz.
- **Cursor:** dibujado, con su recorrido y su clic sobre las cajas guardadas.
- **Marco:** la vista de teléfono va dentro de un celular dibujado.
- **Subtítulos:** cortan en las comas.

Para mantener la nitidez, renderizar en 4K (`--resolution 4k` o `portrait-4k`) y bajar a 1080 con lanczos.

## Estructura que funcionó

Comercial de unos 30 segundos:

1. **Gancho antes y después.** El problema en una imagen (mensajes sin responder fuera de horario).
2. **El producto resolviendo.** Pantallas reales: la conversación, la agenda que se llena.
3. **El control en manos de la persona.** Una acción concreta (tomar la conversación).
4. **Cierre con marca.**

## Un kit para varios rubros

Si se van a hacer versiones para distintos rubros, todo lo que cambia va en un único archivo de configuración por rubro (nombre del negocio, conversaciones, turnos, frases) y el resto es común: alta de la cuenta, carga de datos, captura, voz y generador. El generador reutiliza los tiempos de escena del primer video y avisa si una frase nueva no entra en su lugar.

## Antes de publicar

Revisar cada captura buscando lo que no debe salir: datos de personas reales, direcciones internas, nombres de clientes, funciones que todavía no existen. Los datos de demostración tienen que ser inventados de punta a punta.
