# Explicadores

Un explicador cuenta cómo funciona algo en 30 a 40 segundos. El riesgo es llenar la pantalla de texto y repetir con imágenes lo que ya dice la voz. Este método lo evita.

## Primero el plan, después la animación

Antes de escribir una línea de código se arma un `PLAN.md` con una tabla: un bloque por frase de la locución y, para cada uno, **una sola acción visual**.

Parte del plan de "Es como contratar a alguien nuevo":

| # | Frase | Acción visual (una) | Palabra que la dispara | En pantalla |
| --- | --- | --- | --- | --- |
| 1 | Sumar un agente de IA es como contratar a alguien nuevo. | La credencial cae colgada de su cinta y se balancea. | "contratar" | Tu nuevo empleado |
| 3 | Nada se aplica hasta que lo revisás. | Un sello de aprobado golpea la credencial y queda pegado. | "revisás" | Vos lo revisás |
| 5 | y un evaluador le pone nota, de 0 a 100. | Los clientes se apagan y sube la marca de una regla de 0 a 100. | "nota" | Nota 0 a 100 |
| 7 | Atiende y agenda turnos, las 24 horas. | Un dial de 24 horas da la vuelta completa, del sol a la luna. | "atiende" | 24 h |

Si un bloque necesita dos acciones para entenderse, se parte en dos.

## Las reglas

1. **Una acción visual por bloque.**
2. **Máximo cuatro palabras en pantalla por escena**, sin contar los subtítulos. La voz explica; la pantalla muestra.
3. **Analogía dibujada literal.** Si la idea es "un agente es un empleado nuevo", se dibuja una credencial de empleado. No un ícono abstracto.
4. **Un elemento que persiste.** La credencial no desaparece nunca: cambia de tamaño, se llena y se mueve de escena en escena. El ojo sigue un solo objeto.
5. **Escalas para las cantidades.** Seis casilleros para seis clientes de prueba, una regla de 0 a 100 para una nota, un dial de 24 marcas para las 24 horas.
6. **Foco.** Lo secundario baja al 15 % de opacidad y lo principal se acerca.
7. **Cada acción cae en su palabra.** La animación arranca en el instante en que la voz dice la palabra clave, no al principio de la frase.

El plan también anota **de dónde sale cada dato** (el folleto, el producto), para no afirmar nada que no esté respaldado.

## Sincronizar con la palabra

El generador busca la palabra dentro de los tiempos de la voz y falla si no la encuentra, así un cambio de guion no deja una animación colgada:

```js
// W(línea, "palabra") → segundo en que se dice esa palabra
const W = (i, txt, fin = false) => {
  const k = L[i].words.findIndex((w) => w.text.toLowerCase().startsWith(txt.toLowerCase()));
  if (k < 0) throw new Error(`${txt} no está en ${L[i].id}`);
  return VS[i] + L[i].words[k][fin ? "end" : "start"];
};
```

`L` son las líneas con sus palabras y `VS` el segundo en que arranca cada línea. El mismo generador verifica que la cantidad de palabras en pantalla coincida con la de palabras habladas.

## Versión muda y versión hablada

Un explicador de pasos puede tener las dos:

- **Muda (15 s):** los pasos con texto en pantalla y música. Para carruseles y anuncios.
- **Hablada (25 s):** la misma composición, sin los textos largos, con los tiempos recalculados a partir de la voz y subtítulos con la palabra activa resaltada.

La hablada se genera desde una copia de la base sin voz; no se mantiene como un proyecto aparte.

## De dónde sale el contenido

Del material que ya existe: un folleto, la página del producto, el manual. El explicador no inventa funciones ni promesas; ordena lo que el producto ya hace en tres o cuatro pasos.
