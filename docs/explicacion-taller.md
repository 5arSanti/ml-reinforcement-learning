# Qué hicimos en el taller (en simple)

El profesor nos dio un cuaderno de Colab sobre **aprendizaje por refuerzo**: un agente prueba, recibe premio o castigo, y va aprendiendo qué hacer.

Nosotros **no reescribimos la clase**. Solo respondimos el taller al final del mismo archivo: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`.

---

## En dos frases

1. Movimos **un dial** cada vez (cuánto pruebas, cuánto miras el futuro, cuánto resbala el robot, si el paso cuesta, y qué tan rápido cree en lo último).
2. Cada pregunta dejó **una gráfica o un número** y **una explicación** en lenguaje de desarrollo (PRs, arquitectura, producción). Odoo solo entra como tablero de tareas, no como inventario.

---

## Dónde está cada cosa

| En el cuaderno | Qué es |
|---|---|
| Después del bandido | Tu respuesta de vida real: explorar vs explotar en PRs y refactors |
| Después de Q-learning vs SARSA | Tu respuesta: en producción prefieres la ruta segura (SARSA) |
| Al final, “Respuestas del taller” | Las 5 preguntas con código, gráfica y frase |

---

## Las 5 preguntas, en cristiano

### 1. Bandido (ε)

**Qué pedía el profesor:** ¿qué pasa con ε = 0.5? ¿y si la exploración baja con el tiempo (1/√t)?

**Qué corrimos:** 300 casinos, 1000 jugadas cada uno.

**Qué salió:**

- ε = 0.5: gana **0.569** y al final acierta la mejor máquina el **58.3 %**.
- 1/√t: gana **1.023** y acierta el **88.8 %**.

**Qué significa:** si pruebas la mitad de las veces *para siempre*, nunca dejas de pagar el costo. Si pruebas mucho al inicio y luego te quedas con lo que funciona, ganas más. Como un spike al arrancar el PR y después no cambiar de librería en cada commit.

### 2. Descuento (γ)

**Qué pedía:** entrenar la bodega con γ = 0.5 y γ = 0.99. ¿Cambia la ruta?

**Qué salió:** **sí cambia**. Las dos llegan al despacho en **9 pasos**, pero el último tramo es distinto. El retorno de los últimos 300 episodios: **8.58** vs **8.93**.

**Qué significa:** γ es “cuánto te importa el después”. Bajo = mergear el PR de hoy sin mirar el acoplamiento. Alto = no romper el core la semana que viene.

### 3. Resbalón

**Qué pedía:** `Bodega(resbalon=0.4)` y la política **óptima** (no Q-learning). ¿Se aleja más de X?

**Qué salió:** sí, un poco. La distancia media al paso siguiente: **2.864 → 2.955**. **1** celda apunta más lejos de X. Las rutas siguen en 9 pasos.

**Qué significa:** si el robot a veces no va a donde le dijiste (como un deploy que no sale igual que en local), lo inteligente es no pegarse al peligro.

### 4. Recompensa (costo del paso)

**Qué pedía:** pasar el costo de −1 a 0. ¿Sigue buscando el camino corto?

**Qué salió:** con −1 y con 0 la ruta tiene **9 pasos** y llega a D. En **esta** corrida sí encontró un camino corto; solo cambió la última esquina. La bodega de clase sigue cobrando −1.

**Qué significa:** en teoría, si el tiempo no se castiga, da igual dar vueltas. Aquí el número no mostró que se haya puesto a vagar. Reportamos lo que salió, no lo que “debería” salir.

### 5. Tasa de aprendizaje (α)

**Qué pedía:** comparar α = 0.01, 0.1 y 0.9.

**Qué salió** (retorno medio de los últimos 300 episodios):

- 0.01 → **8.12** (lento)
- 0.1 → **8.54** (el mejor)
- 0.9 → **2.65** (se cae)

**Qué significa:** α es cuánto le crees a lo último que te pasó. Muy bajo = casi no ajustas el código. Muy alto = reescribes el módulo por un bug aislado. 0.1 es el punto medio del cuaderno.

---

## Cómo usarlo en clase

1. Corre el cuaderno de arriba abajo (o ábrelo ya ejecutado).
2. Si preguntan “en su vida”, lee la celda del bandido (PRs / arquitectura).
3. Si preguntan “carro autónomo / dinero real”, lee la de SARSA (producción, feature flag, no el atajo).
4. Si preguntan un número, está en la frase debajo de cada gráfica.

No hace falta volver a entrenar para explicar: los números ya están impresos.
