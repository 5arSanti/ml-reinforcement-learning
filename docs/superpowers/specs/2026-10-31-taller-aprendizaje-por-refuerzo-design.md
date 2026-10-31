# Taller Aprendizaje por Refuerzo — diseño

Fecha: 2026-10-31  
Curso: Machine Learning · Universidad Libre · Prof. Gustavo Santos  
Fuente: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb` (sección 6 + dos preguntas de discusión)  
Enfoque aprobado: mismo notebook, funciones de clase intactas, bloque de respuestas al final

## 1. Problema

El cuaderno enseña bandido multibrazo, GridWorld (`Bodega`), iteración de valores, Q-learning y el acantilado (Q-learning vs SARSA). El taller pide **evidencia** (gráfica o número) y **una frase** por cada una de cinco preguntas. Además hay que responder, en primera persona, las dos preguntas de discusión de las lecturas.

No se entrega un notebook nuevo ni se reescribe el material de clase. Las respuestas viven en el mismo archivo.

## 2. Criterio de éxito

El cuaderno, ejecutado de arriba abajo con `numpy`, `matplotlib` y `pandas`, deja:

- Una respuesta en markdown tras cada pregunta de discusión.
- Cinco bloques de taller, cada uno con figura o `print` y **exactamente una** frase de interpretación en español.
- Las funciones originales `bandido`, `Bodega`, `q_learning` e `iteracion_valores` con la misma firma y el mismo comportamiento que hoy.
- Tras el taller, `Bodega().recompensa(Bodega().inicio) == -1`, y `bandido(..., epsilon=0.0, jugadas=1)` sigue funcionando (el primer argumento de ε es un número, no una función).

Semilla global ya definida en el cuaderno: `SEMILLA = 2026`. Toda corrida estocástica del taller la reutiliza.

## 3. Fuera de alcance

- Rehacer o comentar las secciones 1–5 de teoría.
- Experimentos extra en el acantilado (solo la discusión).
- PDF, bitácora en papel, repo nuevo o cambio de nombre del `.ipynb`.
- Forzar una conclusión que el experimento no muestre (si γ no cambia la ruta, se dice que no cambia).

Los ejemplos de Odoo se pueden editar después sin reabrir este diseño experimental.

## 4. Archivo y anclaje de celdas

Un solo archivo: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`.

Las celdas 0–18 actuales no se reescriben. Eso incluye la celda semilla de γ (pregunta 2 del profesor). Esa celda queda como demo; la respuesta calificable de γ se repite en el bloque final, con frase.

No usar números de celda como ancla (se desplazan al insertar). Insertar así:

| Contenido nuevo | Ancla (texto que ya existe) |
|---|---|
| Discusión del bandido | Markdown que termina en «¿en qué decisiones de su vida o de una empresa aparece este dilema?» |
| Discusión Q-learning vs SARSA | Markdown que termina en «si el agente fuera un carro autónomo o un robot de trading entrenando con dinero real, ¿cuál preferiría?» |
| Bloque «Respuestas del taller» | Inmediatamente **después** de la celda de código que itera `γ` en `[0.5, 0.99]` |

## 5. Componentes (helpers locales)

Una celda de utilidades al inicio del bloque final. No parchea clases ni funciones de las secciones 1–5.

### 5.1 `bandido_eps(epsilon_fn, pagos_reales, jugadas=1000, rng=None)`

Misma lógica que `bandido` (promedio incremental, empates al azar, pago `normal(media, 1)`), pero `epsilon_fn(t)` recibe el índice **1-based** de la jugada.

`ε_t = 1/√t` se implementa como `1 / sqrt(t)` con `t = 1 … jugadas`. En un `for t0 in range(jugadas)` eso es `1 / sqrt(t0 + 1)`. Queda prohibido `1/sqrt(t0)` con `t0 = 0` (división por cero).

`ε = 0.5` constante es `lambda t: 0.5`.

Protocolo idéntico a la demo: 300 repeticiones, 1000 jugadas, `pagos ~ normal(0, 1, 5)`, `rng` de `SEMILLA`.

### 5.2 `BodegaCosto(costo_paso=0)`

Subclase de `Bodega`. Solo redefine `recompensa`: `D → +20`, `X → -20`, celda libre → `costo_paso`. La instancia `Bodega()` original no cambia.

No se añade un argumento nuevo a `Bodega.__init__`.

### 5.3 Reutilización

El taller llama a `q_learning`, `iteracion_valores`, `dibujar` y `ruta_greedy` tal como están. Entrenamientos de bodega: **5000 episodios**, resto de hiperparámetros por defecto salvo el que la pregunta pide variar.

Si una curva queda ilegible, se suaviza con media móvil (como la demo, ventana 100 en Q-learning y 20 en el bandido). No se inventan números.

## 6. Flujo por pregunta

### 6.1 Discusión — bandido (primera persona, Odoo)

Texto aprobado (editable después por el estudiante):

> En Odoo me pasa cuando un flujo de inventario o facturación ya “funciona” (explotar) y alguien propone un módulo nuevo o un refactor (explorar). Si nunca pruebo, me quedo con el primer enfoque que dio resultado, aunque no sea el mejor. Si exploro todo el tiempo —cambiar de librería cada sprint— pago el costo de máquinas malas: regresiones y tiempo. En la práctica uso un ε bajo: dejo un porcentaje chico de capacidad para probar, y el resto lo dejo en lo que ya medí que funciona.

### 6.2 Discusión — Q-learning vs SARSA (primera persona, Odoo)

Texto aprobado:

> Si yo entrenara un agente que mueve existencias reales o dispara asientos en producción, preferiría **SARSA**. Q-learning aprende la ruta óptima pegada al riesgo (el “acantilado”: validar mal un picking, pisar una zona X). Mientras el agente sigue explorando, esa política óptima se cae. SARSA aprende lo que *de verdad hace*, exploración incluida, y se aleja del borde. Con dinero o inventario real quiero la política segura, no la más corta en el simulador.

### 6.3 Pregunta 1 — Bandido

Comparar solo dos estrategias: `ε = 0.5` constante y `ε_t = 1/√t`. No replotear `ε ∈ {0, 0.01, 0.1, 0.3}` de la demo.

Evidencia: dos curvas (recompensa suavizada y % de mejor máquina) y un `print` con recompensa media y % de acierto en las últimas 100 jugadas, para cada estrategia.

Hipótesis (se reescribe si el número dice otra cosa): `0.5` explora de más todo el tiempo; `1/√t` explora al inicio y luego explota.

### 6.4 Pregunta 2 — Descuento γ

`q_learning(Bodega(), gamma=g, episodios=5000)` para `g ∈ {0.5, 0.99}`. Dos mapas con `dibujar` + `ruta_greedy`. Imprimir si las dos rutas (secuencias de estados) son iguales.

Hipótesis: `γ = 0.5` es miope y **puede** cambiar la ruta frente a `0.99`. Si no cambia, la frase lo dice y explica con el retorno o los valores, sin forzar un “sí”.

La celda semilla del profesor no se borra ni se convierte en la respuesta.

### 6.5 Pregunta 3 — Resbalón

Política **óptima** con `iteracion_valores`, no Q-learning.

- `env_lo = Bodega(resbalon=0.1)` (default del cuaderno)
- `env_hi = Bodega(resbalon=0.4)`

Mapas lado a lado. Métrica explícita de “¿se aleja más de X?”:

1. Localizar el estado de `X` con `_buscar("X")`.
2. Para cada celda libre (`S` o `.`), tomar el sucesor determinista `_mover(s, π[s])` y su distancia Manhattan a `X`.
3. Reportar la distancia Manhattan media al sucesor, y cuántas celdas libres eligen un sucesor **estrictamente más lejos** de X con `resbalon=0.4` que con `0.1`.
4. Además, longitud de `ruta_greedy` en cada política (si termina).

Hipótesis: sí se aleja más. Si la cuenta es 0, la frase reporta 0 y lo que sí cambió (valores o ruta).

### 6.6 Pregunta 4 — Costo por paso 0

Entrenar Q-learning 5000 episodios en `Bodega()` (costo −1) y en `BodegaCosto(costo_paso=0)`. Comparar `ruta_greedy` (tope 40 pasos, el default actual).

Evidencia: dos mapas + longitud de cada ruta. Si la de costo 0 no llega a `D` en 40 pasos, eso cuenta como “ya no busca el camino corto”.

Hipótesis: con costo 0 cualquier camino a `D` que evite `X` vale +20; el robot deja de acortar.

No se edita `Bodega.recompensa` en el cuerpo de la clase.

### 6.7 Pregunta 5 — Tasa de aprendizaje

Tres corridas `q_learning(Bodega(), alpha=a, episodios=5000)` con `a ∈ {0.01, 0.1, 0.9}` y la misma `SEMILLA`.

Evidencia: una figura con tres curvas (retorno crudo opcional en gris; media móvil 100 en color) y el retorno medio de los **últimos 300** episodios por cada `α`.

Hipótesis: `0.01` lento, `0.1` equilibrio del cuaderno, `0.9` rápido y ruidoso. La frase nombra el `α` con mejor retorno estable en esos últimos 300.

## 7. Forma de cada respuesta de taller

Orden fijo por pregunta:

1. Título markdown (`### 1. Bandido`, etc.).
2. Celda de código que produce la figura y/o el número.
3. Markdown de **una** frase, escrita **después** de ver la salida real.

Prohibido dejar “TBD”, “pendiente” o una frase que cite un número que no aparezca en el `print` o la figura de esa pregunta.

## 8. Manejo de errores y casos borde

| Caso | Qué hacer |
|---|---|
| `1/√t` con `t=0` | No ocurre: `t` es 1-based |
| Ruta greedy cíclica (costo 0) | Cortar en `max_pasos=40`; reportar que no termina |
| γ no cambia la ruta | Frase: no cambia + por qué (valores / horizonte corto vs mapa chico) |
| `α = 0.01` no converge en 5000 | Eso es la evidencia; no subir episodios salvo gráfica ilegible |
| Gráfica ilegible | Solo suavizar; no cambiar el enunciado |
| Re-ejecución top-to-bottom | Helpers al final no mutan `Bodega` ni `bandido` |

## 9. Verificación

Antes de dar por cerrado el trabajo:

1. Ejecutar el cuaderno completo (local; el mismo código debe correr en Colab sin dependencias nuevas).
2. Celda de chequeo al final del taller que imprime y afirma: `Bodega().recompensa(Bodega().inicio) == -1` y una llamada `bandido(0.0, pagos, jugadas=1, rng=rng)` sin error. No rehacer las 300 repeticiones de la demo.
3. Contar: 2 markdowns de discusión + 5 frases de taller.
4. No hay celdas del taller sin salida (figura o print).

## 10. Decisiones cerradas

- Entregable: el mismo `Aprendizaje_por_Refuerzo_Colab.ipynb`.
- Alcance: taller (5) + discusiones (2).
- Tono: primera persona, contexto software/Odoo, ajustable después.
- Estrategia: helpers locales; no editar funciones de clase.
- Episodios de bodega: 5000.
- `ε_t = 1/√t` con `t` 1-based.
- Pregunta 3 usa iteración de valores.
- Pregunta 4 usa subclase, no un parche a `Bodega`.
- La evidencia manda sobre la hipótesis.
