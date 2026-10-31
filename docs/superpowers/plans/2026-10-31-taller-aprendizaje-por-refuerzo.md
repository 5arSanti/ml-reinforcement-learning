# Taller Aprendizaje por Refuerzo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Completar en el mismo cuaderno las 5 preguntas del taller (evidencia + una frase) y las 2 discusiones en primera persona, sin reescribir las celdas de clase.

**Architecture:** Las celdas 0–18 actuales no se editan. Se insertan markdowns de discusión junto a cada pregunta de lectura. Al final, después de la celda semilla de γ, un bloque «Respuestas del taller» con helpers locales (`bandido_eps`, `BodegaCosto`) y un experimento por pregunta. Tests locales cargan solo definiciones del `.ipynb` (no reentrenan el acantilado).

**Tech Stack:** Python 3, numpy, matplotlib, pandas (ya importado en el cuaderno), pytest (solo local).

## Global Constraints

- Entregable: el mismo `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`.
- No reescribir las celdas 0–18 actuales (incluye la semilla de γ).
- No añadir dependencias nuevas al cuaderno: solo `numpy`, `matplotlib`, `pandas`.
- Semilla: `SEMILLA = 2026` en toda corrida estocástica del taller.
- Episodios de bodega: `5000`. Resto de hiperparámetros de `q_learning` por defecto, salvo el que la pregunta varía.
- `ε_t = 1/√t` con `t` 1-based (`1 / sqrt(t0 + 1)`). Prohibido `1/sqrt(0)`.
- Pregunta 3: `iteracion_valores`, no Q-learning. `Bodega(resbalon=0.4)` vs `0.1`.
- Pregunta 4: subclase `BodegaCosto`; no editar `Bodega.recompensa`.
- Cada pregunta 1–5: título markdown + código + **exactamente una** frase, escrita después de ver el `print`/figura. Prohibido TBD, pendiente o un número que no salga en esa celda.
- La evidencia manda sobre la hipótesis (si γ no cambia la ruta, se dice que no cambia).
- Tras el taller: `Bodega().recompensa(Bodega().inicio) == -1` y `bandido(0.0, pagos, jugadas=1, rng=rng)` sin error.
- Discusiones: textos aprobados en `docs/superpowers/specs/2026-10-31-taller-aprendizaje-por-refuerzo-design.md` §§6.1–6.2.
- Anclas de inserción: ver spec §4. No usar índices de celda.
- Fuera de alcance: rehacer teoría 1–5, experimentos extra del acantilado, PDF, renombrar el `.ipynb`.

## File structure

| Path | Responsibility |
|---|---|
| `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb` | Único entregable. Discusiones + bloque del taller. |
| `tests/nb_edit.py` | Insertar celdas después de un ancla de texto. |
| `tests/notebook_ns.py` | Ejecutar solo imports/defs/clases del cuaderno (tests rápidos). |
| `tests/test_taller_celdas.py` | Presencia de discusiones, semilla de γ intacta, 5 frases, chequeo. |
| `tests/test_taller_helpers.py` | Contratos de `bandido_eps`, `BodegaCosto` y métrica de alejamiento. |
| `docs/superpowers/specs/2026-10-31-taller-aprendizaje-por-refuerzo-design.md` | Spec. Solo lectura. |

No extraer `Bodega` ni `q_learning` a un `.py` de producción: el profesor corre Colab.

---

### Task 1: Discusiones junto a las lecturas

**Files:**
- Create: `tests/nb_edit.py`
- Create: `tests/test_taller_celdas.py`
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb` (solo insertar 2 markdowns; no editar celdas existentes)

**Interfaces:**
- Consumes: anclas de la spec §4 (substrings ya presentes en el cuaderno).
- Produces: `insert_after_anchor(nb_path, anchor, new_cells) -> None`; `append_cells(nb_path, new_cells) -> None`; dos celdas markdown con el texto aprobado.

- [ ] **Step 1: Write the failing test**

Create `tests/test_taller_celdas.py`:

```python
import json
from pathlib import Path

NB = Path("scripts/Aprendizaje_por_Refuerzo_Colab.ipynb")


def cell_sources():
    nb = json.loads(NB.read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in nb["cells"]]


def test_celda_semilla_gamma_intacta():
    assert any("for ax, g in zip(axs, [0.5, 0.99])" in s for s in cell_sources())


def test_discusion_bandido_odoo():
    assert any("flujo de inventario o facturación" in s for s in cell_sources())


def test_discusion_sarsa_odoo():
    blob = "\n".join(cell_sources())
    assert "preferiría" in blob and "SARSA" in blob
    assert "existencias reales" in blob
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_celdas.py -v`

Expected: `test_celda_semilla_gamma_intacta` PASS. `test_discusion_bandido_odoo` FAIL (`assert False` / not found). `test_discusion_sarsa_odoo` FAIL.

- [ ] **Step 3: Write `tests/nb_edit.py`**

```python
import json
from pathlib import Path


def load_nb(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_nb(path, nb):
    Path(path).write_text(
        json.dumps(nb, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def markdown_cell(text):
    src = text if text.endswith("\n") else text + "\n"
    return {"cell_type": "markdown", "metadata": {}, "source": [src]}


def code_cell(text):
    src = text if text.endswith("\n") else text + "\n"
    return {
        "cell_type": "code",
        "metadata": {},
        "source": [src],
        "execution_count": None,
        "outputs": [],
    }


def insert_after_anchor(nb_path, anchor, new_cells):
    nb = load_nb(nb_path)
    idx = None
    for i, cell in enumerate(nb["cells"]):
        if anchor in "".join(cell["source"]):
            idx = i
            break
    if idx is None:
        raise ValueError(f"Anchor not found: {anchor!r}")
    for offset, cell in enumerate(new_cells, start=1):
        nb["cells"].insert(idx + offset, cell)
    save_nb(nb_path, nb)


def append_cells(nb_path, new_cells):
    nb = load_nb(nb_path)
    nb["cells"].extend(new_cells)
    save_nb(nb_path, nb)
```

- [ ] **Step 4: Insert the two discussion cells**

From repo root (`ml-reinforcement-learning/`):

```bash
python - <<'PY'
from tests.nb_edit import insert_after_anchor, markdown_cell

nb = "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb"

insert_after_anchor(
    nb,
    "¿en qué decisiones de su vida o de una empresa aparece este dilema?",
    [markdown_cell(
        "**Respuesta.** En Odoo me pasa cuando un flujo de inventario o facturación ya "
        "“funciona” (explotar) y alguien propone un módulo nuevo o un refactor (explorar). "
        "Si nunca pruebo, me quedo con el primer enfoque que dio resultado, aunque no sea "
        "el mejor. Si exploro todo el tiempo —cambiar de librería cada sprint— pago el "
        "costo de máquinas malas: regresiones y tiempo. En la práctica uso un ε bajo: "
        "dejo un porcentaje chico de capacidad para probar, y el resto lo dejo en lo que "
        "ya medí que funciona."
    )],
)

insert_after_anchor(
    nb,
    "si el agente fuera un carro autónomo o un robot de trading entrenando con dinero real, ¿cuál preferiría?",
    [markdown_cell(
        "**Respuesta.** Si yo entrenara un agente que mueve existencias reales o dispara "
        "asientos en producción, preferiría **SARSA**. Q-learning aprende la ruta óptima "
        "pegada al riesgo (el “acantilado”: validar mal un picking, pisar una zona X). "
        "Mientras el agente sigue explorando, esa política óptima se cae. SARSA aprende "
        "lo que *de verdad hace*, exploración incluida, y se aleja del borde. Con dinero "
        "o inventario real quiero la política segura, no la más corta en el simulador."
    )],
)
print("ok")
PY
```

Do not modify the two lecture markdowns that contain the questions. Do not touch the γ starter cell.

- [ ] **Step 5: Run the tests and make sure they pass**

Run: `python -m pytest tests/test_taller_celdas.py -v`

Expected: 3 PASS.

- [ ] **Step 6: Commit**

```bash
git add tests/nb_edit.py tests/test_taller_celdas.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add first-person discussion answers next to the lecture questions.

EOF
)"
```

---

### Task 2: Helpers locales (`bandido_eps`, `BodegaCosto`, alejamiento)

**Files:**
- Create: `tests/notebook_ns.py`
- Create: `tests/test_taller_helpers.py`
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb` (insertar título + celda de helpers **después** de la celda que contiene `for ax, g in zip(axs, [0.5, 0.99])`)

**Interfaces:**
- Consumes: `Bodega`, `bandido` already defined in the lecture cells; `insert_after_anchor` and `append_cells` from Task 1.
- Produces:
  - `load_defs() -> dict` namespace with lecture + helper defs.
  - `bandido_eps(epsilon_fn, pagos_reales, jugadas=1000, rng=None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]`
  - `class BodegaCosto(Bodega)` with `__init__(self, costo_paso=0, resbalon=0.1)` and `recompensa(self, s2)`
  - `manhattan_estado(env, s, t) -> int`
  - `media_dist_sucesor(env, politica) -> float`
  - `n_celdas_mas_lejos(env, pi_lo, pi_hi) -> int`
  - `ruta_llego_a_terminal(env, ruta) -> bool`

- [ ] **Step 1: Write the failing test**

Create `tests/notebook_ns.py`:

```python
import ast
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

NB = Path("scripts/Aprendizaje_por_Refuerzo_Colab.ipynb")
KEEP_ASSIGN = {"SEMILLA", "ROJO", "NARANJA", "NEGRO", "GRIS"}


def _keep_node(node):
    if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
        return True
    if isinstance(node, ast.Assign):
        return all(
            isinstance(t, ast.Name) and t.id in KEEP_ASSIGN for t in node.targets
        )
    return False


def load_defs():
    nb = json.loads(NB.read_text(encoding="utf-8"))
    ns = {"__name__": "notebook_defs"}
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        body = [n for n in tree.body if _keep_node(n)]
        if not body:
            continue
        exec(compile(ast.Module(body=body, type_ignores=[]), "<nb>", "exec"), ns)
    return ns
```

Create `tests/test_taller_helpers.py`:

```python
import math

import numpy as np

from tests.notebook_ns import load_defs


def test_bandido_eps_t_is_one_based_and_no_div_zero():
    ns = load_defs()
    seen = []

    def epsilon_fn(t):
        seen.append(t)
        return 1.0 / math.sqrt(t)

    rng = np.random.default_rng(2026)
    ns["bandido_eps"](epsilon_fn, np.array([0.0, 1.0, 0.0, 0.0, 0.0]), jugadas=8, rng=rng)
    assert seen[0] == 1
    assert seen == list(range(1, 9))


def test_bodega_original_sigue_en_menos_uno():
    ns = load_defs()
    env = ns["Bodega"]()
    assert env.recompensa(env.inicio) == -1


def test_bodega_costo_cero_en_celda_libre():
    ns = load_defs()
    env = ns["BodegaCosto"](costo_paso=0)
    assert env.recompensa(env.inicio) == 0
    assert env.recompensa(env._buscar("D")) == 20
    assert env.recompensa(env._buscar("X")) == -20


def test_manhattan_y_alejamiento():
    ns = load_defs()
    env = ns["Bodega"]()
    x = env._buscar("X")
    assert ns["manhattan_estado"](env, x, x) == 0
    pi = np.zeros(env.n_estados, dtype=int)
    media = ns["media_dist_sucesor"](env, pi)
    assert media >= 0
    assert ns["n_celdas_mas_lejos"](env, pi, pi) == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_helpers.py -v`

Expected: FAIL with `KeyError: 'bandido_eps'` (or `BodegaCosto`).

- [ ] **Step 3: Insert helpers cell**

```bash
python - <<'PY'
from tests.nb_edit import insert_after_anchor, markdown_cell, code_cell

nb = "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb"
insert_after_anchor(
    nb,
    "for ax, g in zip(axs, [0.5, 0.99])",
    [
        markdown_cell("## Respuestas del taller\n\nHelpers locales: no modifican `bandido` ni `Bodega` de las secciones anteriores."),
        code_cell(r'''
def bandido_eps(epsilon_fn, pagos_reales, jugadas=1000, rng=None):
    """Igual que bandido, pero ε = epsilon_fn(t) con t = 1..jugadas."""
    k = len(pagos_reales)
    Q = np.zeros(k)
    N = np.zeros(k)
    mejor = np.argmax(pagos_reales)
    recompensas, acierto = np.zeros(jugadas), np.zeros(jugadas)
    for t0 in range(jugadas):
        t = t0 + 1
        if rng.random() < epsilon_fn(t):
            a = rng.integers(k)
        else:
            a = rng.choice(np.flatnonzero(Q == Q.max()))
        r = rng.normal(pagos_reales[a], 1.0)
        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        recompensas[t0], acierto[t0] = r, (a == mejor)
    return recompensas, acierto, Q, N


class BodegaCosto(Bodega):
    """Bodega con costo de paso configurable. No toca Bodega.recompensa."""

    def __init__(self, costo_paso=0, resbalon=0.1):
        super().__init__(resbalon=resbalon)
        self.costo_paso = costo_paso

    def recompensa(self, s2):
        return {"D": 20, "X": -20}.get(self.celda(s2), self.costo_paso)


def manhattan_estado(env, s, t):
    f1, c1 = divmod(s, env.cols)
    f2, c2 = divmod(t, env.cols)
    return abs(f1 - f2) + abs(c1 - c2)


def media_dist_sucesor(env, politica):
    x = env._buscar("X")
    dists = [
        manhattan_estado(env, env._mover(s, int(politica[s])), x)
        for s in range(env.n_estados)
        if env.celda(s) in "S."
    ]
    return float(np.mean(dists))


def n_celdas_mas_lejos(env, pi_lo, pi_hi):
    x = env._buscar("X")
    n = 0
    for s in range(env.n_estados):
        if env.celda(s) not in "S.":
            continue
        d_lo = manhattan_estado(env, env._mover(s, int(pi_lo[s])), x)
        d_hi = manhattan_estado(env, env._mover(s, int(pi_hi[s])), x)
        if d_hi > d_lo:
            n += 1
    return n


def ruta_llego_a_terminal(env, ruta):
    return env.terminal(ruta[-1])
'''),
    ],
)
print("ok")
PY
```

- [ ] **Step 4: Run the tests and make sure they pass**

Run: `python -m pytest tests/test_taller_helpers.py tests/test_taller_celdas.py -v`

Expected: all PASS. `test_celda_semilla_gamma_intacta` still PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/notebook_ns.py tests/test_taller_helpers.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add local workshop helpers without changing Bodega or bandido.

EOF
)"
```

---

### Task 3: Pregunta 1 — Bandido

**Files:**
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb` (3 celdas al final: título, código, frase)
- Modify: `tests/test_taller_celdas.py` (assert del título y de que la frase cita un número)

**Interfaces:**
- Consumes: `bandido_eps(epsilon_fn, pagos_reales, jugadas=1000, rng=None)`
- Produces: figura 1×2; print `ε = ... recompensa media = ... mejor máquina en las últimas 100 = ... %` para `0.5` y `1/√t`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_taller_celdas.py`:

```python
def test_pregunta1_titulo_y_frase_con_numero():
    blob = "\n".join(cell_sources())
    assert "### 1. Bandido" in blob
    # la frase vive en un markdown distinto al título y contiene un dígito
    frases = [
        s for s in cell_sources()
        if s.startswith("**Frase.**") and "Bandido" not in s.split("\n")[0]
    ]
    assert any(
        any(ch.isdigit() for ch in s) and ("0.5" in s or "√" in s or "sqrt" in s)
        for s in cell_sources()
        if s.startswith("**Frase.**")
    )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_celdas.py::test_pregunta1_titulo_y_frase_con_numero -v`

Expected: FAIL (`### 1. Bandido` missing).

- [ ] **Step 3: Insert title + experiment cell (no phrase yet)**

Append at the end of the notebook (helpers are already the last cells):

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell, code_cell

append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [
        markdown_cell("### 1. Bandido"),
        code_cell(r'''
rng = np.random.default_rng(SEMILLA)
estrategias = {
    "ε = 0.5": lambda t: 0.5,
    "ε = 1/√t": lambda t: 1.0 / np.sqrt(t),
}
resultados_p1 = {}
for nombre, fn in estrategias.items():
    R, A = [], []
    for _ in range(300):
        pagos = rng.normal(0, 1, 5)
        r, a, _, _ = bandido_eps(fn, pagos, rng=rng)
        R.append(r)
        A.append(a)
    resultados_p1[nombre] = (np.mean(R, axis=0), np.mean(A, axis=0) * 100)

fig, axs = plt.subplots(1, 2, figsize=(12, 4.3))
for (nombre, c) in zip(estrategias, [ROJO, NARANJA]):
    r, a = resultados_p1[nombre]
    suav = np.convolve(r, np.ones(20) / 20, mode="valid")
    axs[0].plot(suav, color=c, lw=2, label=nombre)
    axs[1].plot(a, color=c, lw=2, label=nombre)
axs[0].set(title="Recompensa promedio por jugada", xlabel="Jugada", ylabel="Recompensa")
axs[1].set(title="% de veces que eligió la mejor máquina", xlabel="Jugada", ylabel="%")
axs[1].legend(frameon=False)
plt.tight_layout()
plt.show()

for nombre in estrategias:
    r, a = resultados_p1[nombre]
    print(f"{nombre:<12}  recompensa media = {r.mean():.3f}   mejor máquina en las últimas 100 = {a[-100:].mean():.1f} %")
'''),
    ],
)
print("ok")
PY
```

- [ ] **Step 4: Run the experiment and capture prints**

```bash
python - <<'PY'
from tests.notebook_ns import load_defs
ns = load_defs()
# re-ejecuta solo el cuerpo de la pregunta 1 (mismas líneas, sin show)
import numpy as np
rng = np.random.default_rng(ns["SEMILLA"])
estrategias = {"ε = 0.5": lambda t: 0.5, "ε = 1/√t": lambda t: 1.0 / np.sqrt(t)}
for nombre, fn in estrategias.items():
    R, A = [], []
    for _ in range(300):
        pagos = rng.normal(0, 1, 5)
        r, a, _, _ = ns["bandido_eps"](fn, pagos, rng=rng)
        R.append(r); A.append(a)
    r, a = np.mean(R, axis=0), np.mean(A, axis=0) * 100
    print(f"{nombre:<12}  recompensa media = {r.mean():.3f}   mejor máquina en las últimas 100 = {a[-100:].mean():.1f} %")
PY
```

Expected: two lines with finite numbers. Do not type numbers from memory.

- [ ] **Step 5: Write the one-sentence markdown**

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell
# Reemplaza M1, P1, M2, P2 por los cuatro números del Step 4 (mismo formato .3f / .1f).
append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [markdown_cell(
        "**Frase.** Con ε = 0.5 la recompensa media es M1 y acierta P1 % al final; "
        "con 1/√t la media es M2 y acierta P2 % porque deja de explorar cuando ya vio la mejor máquina."
    )],
)
print("ok")
PY
```

If `1/√t` has **worse** mean or worse last-100 than `0.5`, keep the numbers and say that: do not invent the hypothesis.

- [ ] **Step 6: Run tests**

Run: `python -m pytest tests/test_taller_celdas.py tests/test_taller_helpers.py -v`

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add tests/test_taller_celdas.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add bandit workshop evidence for constant 0.5 vs 1/sqrt(t).

EOF
)"
```

---

### Task 4: Pregunta 2 — Descuento γ

**Files:**
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`
- Modify: `tests/test_taller_celdas.py`

**Interfaces:**
- Consumes: `q_learning(env, episodios=3000, alpha=0.1, gamma=0.95, ...)`, `dibujar`, `ruta_greedy`
- Produces: `rutas_gamma: dict[float, list[int]]`; print `rutas_iguales=True/False`; two maps.

- [ ] **Step 1: Write the failing test**

Append:

```python
def test_pregunta2_titulo_y_frase():
    blob = "\n".join(cell_sources())
    assert "### 2. Descuento" in blob
    assert any(s.startswith("**Frase.**") and ("γ" in s or "gamma" in s.lower()) for s in cell_sources())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_celdas.py::test_pregunta2_titulo_y_frase -v`

Expected: FAIL.

- [ ] **Step 3: Insert title + experiment**

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell, code_cell

append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [
        markdown_cell("### 2. Descuento"),
        code_cell(r'''
env_p2 = Bodega()
rutas_gamma = {}
Qs_gamma = {}
fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
for ax, g in zip(axs, [0.5, 0.99]):
    Qg, ret_g = q_learning(env_p2, gamma=g, episodios=5000)
    pi_g = Qg.argmax(axis=1)
    ruta_g = ruta_greedy(env_p2, pi_g)
    rutas_gamma[g] = ruta_g
    Qs_gamma[g] = Qg
    dibujar(env_p2, Qg.max(axis=1), pi_g, ruta=ruta_g, titulo=f"Q-learning con γ = {g}", ax=ax)
    print(f"γ = {g}  pasos_ruta = {len(ruta_g) - 1}  retorno medio últimos 300 = {ret_g[-300:].mean():.2f}  termina={ruta_llego_a_terminal(env_p2, ruta_g)}")
print("rutas_iguales", rutas_gamma[0.5] == rutas_gamma[0.99])
plt.tight_layout()
plt.show()
'''),
    ],
)
print("ok")
PY
```

Leave the professor starter cell (`for ax, g in zip(axs, [0.5, 0.99])` **without** `env_p2`) untouched.

- [ ] **Step 4: Run the experiment and capture prints**

```bash
python - <<'PY'
from tests.notebook_ns import load_defs
ns = load_defs()
env = ns["Bodega"]()
rutas = {}
for g in (0.5, 0.99):
    Qg, ret_g = ns["q_learning"](env, gamma=g, episodios=5000)
    ruta = ns["ruta_greedy"](env, Qg.argmax(axis=1))
    rutas[g] = ruta
    print(g, len(ruta) - 1, float(ret_g[-300:].mean()), ns["ruta_llego_a_terminal"](env, ruta))
print("rutas_iguales", rutas[0.5] == rutas[0.99])
PY
```

Expected: three lines. This step can take ~30–60 s.

- [ ] **Step 5: Write the one-sentence markdown**

If `rutas_iguales` is False: say the route **changes** and mention both lengths / last-300 returns from Step 4.

If True: say the route **does not change** and explain with those same numbers (γ bajo no alcanza a diferenciar el horizonte en este mapa, o ambas llegan a D en N pasos).

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell
# Write the real sentence here, including the printed numbers. One sentence only.
append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [markdown_cell("**Frase.** La ruta cambia/no cambia: γ = 0.5 da L1 pasos y retorno R1; γ = 0.99 da L2 pasos y retorno R2.")],
)
print("ok")
PY
```

Replace `cambia/no cambia`, `L1`, `R1`, `L2`, `R2` with Step 4 values before running. Do not leave those tokens in the notebook.

- [ ] **Step 6: Run tests**

Run: `python -m pytest tests/test_taller_celdas.py tests/test_taller_helpers.py -v`

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add tests/test_taller_celdas.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add gamma 0.5 vs 0.99 warehouse routes with one-sentence reading.

EOF
)"
```

---

### Task 5: Pregunta 3 — Resbalón

**Files:**
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`
- Modify: `tests/test_taller_celdas.py`

**Interfaces:**
- Consumes: `iteracion_valores(env, gamma=0.95, tol=1e-6) -> tuple[np.ndarray, np.ndarray, list]`, `media_dist_sucesor`, `n_celdas_mas_lejos`, `ruta_greedy`
- Produces: print `media_sucesor_0.1`, `media_sucesor_0.4`, `n_celdas_mas_lejos`, `len_ruta` for each.

- [ ] **Step 1: Write the failing test**

```python
def test_pregunta3_usa_iteracion_valores():
    blob = "\n".join(cell_sources())
    assert "### 3. Resbalón" in blob
    assert "Bodega(resbalon=0.4)" in blob
    assert "iteracion_valores" in blob
    assert any(s.startswith("**Frase.**") and ("X" in s or "resbal" in s.lower()) for s in cell_sources())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_celdas.py::test_pregunta3_usa_iteracion_valores -v`

Expected: FAIL.

- [ ] **Step 3: Insert title + experiment**

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell, code_cell

append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [
        markdown_cell("### 3. Resbalón"),
        code_cell(r'''
env_lo = Bodega(resbalon=0.1)
env_hi = Bodega(resbalon=0.4)
_, pi_lo, _ = iteracion_valores(env_lo)
_, pi_hi, _ = iteracion_valores(env_hi)
ruta_lo = ruta_greedy(env_lo, pi_lo)
ruta_hi = ruta_greedy(env_hi, pi_hi)

fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
dibujar(env_lo, politica=pi_lo, ruta=ruta_lo, titulo="Óptima con resbalón = 0.1", ax=axs[0])
dibujar(env_hi, politica=pi_hi, ruta=ruta_hi, titulo="Óptima con resbalón = 0.4", ax=axs[1])
plt.tight_layout()
plt.show()

print(f"media_sucesor_0.1 = {media_dist_sucesor(env_lo, pi_lo):.3f}")
print(f"media_sucesor_0.4 = {media_dist_sucesor(env_hi, pi_hi):.3f}")
print(f"n_celdas_mas_lejos = {n_celdas_mas_lejos(env_lo, pi_lo, pi_hi)}")
print(f"len_ruta_0.1 = {len(ruta_lo) - 1}  termina={ruta_llego_a_terminal(env_lo, ruta_lo)}")
print(f"len_ruta_0.4 = {len(ruta_hi) - 1}  termina={ruta_llego_a_terminal(env_hi, ruta_hi)}")
'''),
    ],
)
print("ok")
PY
```

`n_celdas_mas_lejos(env_lo, pi_lo, pi_hi)` uses the same map geometry (both `Bodega` maps are identical). Using `env_lo` for coordinates is correct.

- [ ] **Step 4: Run the experiment and capture prints**

```bash
python - <<'PY'
from tests.notebook_ns import load_defs
ns = load_defs()
env_lo, env_hi = ns["Bodega"](resbalon=0.1), ns["Bodega"](resbalon=0.4)
_, pi_lo, _ = ns["iteracion_valores"](env_lo)
_, pi_hi, _ = ns["iteracion_valores"](env_hi)
print("media", ns["media_dist_sucesor"](env_lo, pi_lo), ns["media_dist_sucesor"](env_hi, pi_hi))
print("n_celdas_mas_lejos", ns["n_celdas_mas_lejos"](env_lo, pi_lo, pi_hi))
print("lens", len(ns["ruta_greedy"](env_lo, pi_lo)) - 1, len(ns["ruta_greedy"](env_hi, pi_hi)) - 1)
PY
```

- [ ] **Step 5: Write the one-sentence markdown**

If `n_celdas_mas_lejos > 0` or `media_sucesor_0.4 > media_sucesor_0.1`: “Sí se aleja más de X: …” with those numbers.

If both are 0 / equal: report 0 and mention whatever did change (ruta length or “la política óptima no cambia las flechas”).

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell
append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [markdown_cell("**Frase.** Sustituye esta oración por una sola frase que cite media_sucesor_0.1, media_sucesor_0.4 y n_celdas_mas_lejos del Step 4.")],
)
print("ok")
PY
```

Do not leave the word `Sustituye` in the notebook.

- [ ] **Step 6: Run tests**

Run: `python -m pytest tests/test_taller_celdas.py tests/test_taller_helpers.py -v`

Expected: all PASS. Confirm the experiment cell contains `iteracion_valores` and **not** `q_learning` for this question (the string `q_learning` may still appear in pregunta 2).

- [ ] **Step 7: Commit**

```bash
git add tests/test_taller_celdas.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add optimal slip-0.4 policy and distance-to-X evidence.

EOF
)"
```

---

### Task 6: Pregunta 4 — Costo por paso 0

**Files:**
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`
- Modify: `tests/test_taller_celdas.py`

**Interfaces:**
- Consumes: `BodegaCosto(costo_paso=0)`, `q_learning(..., episodios=5000)`, `ruta_greedy` (default `max_pasos=40`), `ruta_llego_a_terminal`
- Produces: print `len_ruta_costo_-1`, `len_ruta_costo_0`, `termina` for each.

- [ ] **Step 1: Write the failing test**

```python
def test_pregunta4_subclase_no_parche():
    blob = "\n".join(cell_sources())
    assert "### 4. Recompensas" in blob
    assert "BodegaCosto(costo_paso=0)" in blob
    assert "def recompensa(self, s2):" in blob  # solo en la subclase, ya insertada
    # la clase Bodega original sigue devolviendo -1 en su source
    assert 'return {"D": 20, "X": -20}.get(self.celda(s2), -1)' in blob
    assert any(s.startswith("**Frase.**") and ("costo" in s.lower() or "paso" in s) for s in cell_sources())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_celdas.py::test_pregunta4_subclase_no_parche -v`

Expected: FAIL on `### 4. Recompensas`.

- [ ] **Step 3: Insert title + experiment**

```python
from tests.nb_edit import append_cells, markdown_cell, code_cell

append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [
        markdown_cell("### 4. Recompensas"),
        code_cell(r'''
env_m1 = Bodega()
env_0 = BodegaCosto(costo_paso=0)
Q_m1, _ = q_learning(env_m1, episodios=5000)
Q_0, _ = q_learning(env_0, episodios=5000)
pi_m1, pi_0 = Q_m1.argmax(axis=1), Q_0.argmax(axis=1)
ruta_m1, ruta_0 = ruta_greedy(env_m1, pi_m1), ruta_greedy(env_0, pi_0)

fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
dibujar(env_m1, Q_m1.max(axis=1), pi_m1, ruta=ruta_m1, titulo="Costo por paso = −1", ax=axs[0])
dibujar(env_0, Q_0.max(axis=1), pi_0, ruta=ruta_0, titulo="Costo por paso = 0", ax=axs[1])
plt.tight_layout()
plt.show()

print(f"len_ruta_costo_-1 = {len(ruta_m1) - 1}  termina={ruta_llego_a_terminal(env_m1, ruta_m1)}")
print(f"len_ruta_costo_0 = {len(ruta_0) - 1}  termina={ruta_llego_a_terminal(env_0, ruta_0)}")
print("Bodega_original_inicio", Bodega().recompensa(Bodega().inicio))
'''),
    ],
)
```

- [ ] **Step 4: Run the experiment and capture prints**

```bash
python - <<'PY'
from tests.notebook_ns import load_defs
ns = load_defs()
env_m1, env_0 = ns["Bodega"](), ns["BodegaCosto"](costo_paso=0)
Qm, _ = ns["q_learning"](env_m1, episodios=5000)
Q0, _ = ns["q_learning"](env_0, episodios=5000)
r1 = ns["ruta_greedy"](env_m1, Qm.argmax(axis=1))
r0 = ns["ruta_greedy"](env_0, Q0.argmax(axis=1))
print("m1", len(r1) - 1, ns["ruta_llego_a_terminal"](env_m1, r1))
print("cero", len(r0) - 1, ns["ruta_llego_a_terminal"](env_0, r0))
print("orig", ns["Bodega"]().recompensa(ns["Bodega"]().inicio))
PY
```

Expected: `orig` is `-1`.

- [ ] **Step 5: Write the one-sentence markdown**

If `len_ruta_costo_0 > len_ruta_costo_-1` or `termina` is False for costo 0: the robot **stopped** seeking the short path; quote both lengths.

If lengths are equal and both terminate: say it **still** reached D in N steps (evidence first). Do not claim it wanders if the route is the same.

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell
append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [markdown_cell("**Frase.** Con costo −1 la ruta tiene L1 pasos; con costo 0 tiene L2 pasos y termina=T.")],
)
print("ok")
PY
```

Replace `L1`, `L2`, `T` with Step 4 values.

- [ ] **Step 6: Run tests**

Run: `python -m pytest tests/test_taller_celdas.py tests/test_taller_helpers.py -v`

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add tests/test_taller_celdas.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add step-cost 0 vs -1 routes using BodegaCosto subclass.

EOF
)"
```

---

### Task 7: Pregunta 5 — Tasa de aprendizaje

**Files:**
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`
- Modify: `tests/test_taller_celdas.py`

**Interfaces:**
- Consumes: `q_learning(Bodega(), alpha=a, episodios=5000)` with `SEMILLA` default
- Produces: `medias_alpha: dict[float, float]` last-300 means; one figure with three smoothed curves.

- [ ] **Step 1: Write the failing test**

```python
def test_pregunta5_tres_alphas():
    blob = "\n".join(cell_sources())
    assert "### 5. Tasa de aprendizaje" in blob
    assert "0.01" in blob and "0.9" in blob
    assert any(s.startswith("**Frase.**") and "α" in s for s in cell_sources())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_celdas.py::test_pregunta5_tres_alphas -v`

Expected: FAIL.

- [ ] **Step 3: Insert title + experiment**

```python
from tests.nb_edit import append_cells, markdown_cell, code_cell

append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [
        markdown_cell("### 5. Tasa de aprendizaje"),
        code_cell(r'''
alphas = [0.01, 0.1, 0.9]
colores_a = {0.01: GRIS, 0.1: ROJO, 0.9: NARANJA}
retornos_alpha = {}
fig, ax = plt.subplots(figsize=(10, 4.2))
for a in alphas:
    _, ret = q_learning(Bodega(), alpha=a, episodios=5000)
    retornos_alpha[a] = ret
    media = np.convolve(ret, np.ones(100) / 100, mode="valid")
    ax.plot(np.arange(99, len(ret)), media, color=colores_a[a], lw=2.5, label=f"α = {a}")
ax.set(title="Curva de aprendizaje (media móvil 100)", xlabel="Episodio", ylabel="Retorno")
ax.legend(frameon=False)
plt.tight_layout()
plt.show()

for a in alphas:
    print(f"α = {a:<4}  retorno medio últimos 300 = {retornos_alpha[a][-300:].mean():.2f}")
mejor = max(alphas, key=lambda a: retornos_alpha[a][-300:].mean())
print("mejor_alpha_estable", mejor)
'''),
    ],
)
```

- [ ] **Step 4: Run the experiment and capture prints**

```bash
python - <<'PY'
from tests.notebook_ns import load_defs
ns = load_defs()
for a in (0.01, 0.1, 0.9):
    _, ret = ns["q_learning"](ns["Bodega"](), alpha=a, episodios=5000)
    print(a, float(ret[-300:].mean()))
PY
```

Expected: three floats. ~1 minute.

- [ ] **Step 5: Write the one-sentence markdown**

Name the `α` with the highest last-300 mean and quote all three numbers. If `0.9` is highest but the curve is visually noisier, you may mention noise **in the same sentence**, still one sentence.

```bash
python - <<'PY'
from tests.nb_edit import append_cells, markdown_cell
append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [markdown_cell("**Frase.** El mejor retorno estable de los últimos 300 es α = A (R01 / R1 / R9).")],
)
print("ok")
PY
```

Replace `A`, `R01`, `R1`, `R9` with Step 4 values.

- [ ] **Step 6: Run tests**

Run: `python -m pytest tests/test_taller_celdas.py tests/test_taller_helpers.py -v`

Expected: all PASS.

- [ ] **Step 7: Commit**

```bash
git add tests/test_taller_celdas.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add learning-rate comparison for alpha 0.01, 0.1 and 0.9.

EOF
)"
```

---

### Task 8: Celda de chequeo y conteo de entregables

**Files:**
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb`
- Modify: `tests/test_taller_celdas.py`

**Interfaces:**
- Consumes: original `bandido(epsilon, pagos_reales, jugadas=1000, rng=None)` and `Bodega.recompensa`
- Produces: prints `check_recompensa_inicio True` and `check_bandido_escalar True`

- [ ] **Step 1: Write the failing test**

```python
def test_cinco_frases_y_chequeo():
    sources = cell_sources()
    frases = [s for s in sources if s.startswith("**Frase.**")]
    assert len(frases) == 5
    blob = "\n".join(sources)
    assert "check_recompensa_inicio" in blob
    assert "bandido(0.0," in blob or "bandido(0.0 ," in blob
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_taller_celdas.py::test_cinco_frases_y_chequeo -v`

Expected: FAIL on `check_recompensa_inicio` (5 frases should already exist).

- [ ] **Step 3: Insert check cell after pregunta 5 phrase**

```python
from tests.nb_edit import append_cells, markdown_cell, code_cell

append_cells(
    "scripts/Aprendizaje_por_Refuerzo_Colab.ipynb",
    [
        markdown_cell("### Chequeo: el material de clase no se rompió"),
        code_cell(r'''
env_chk = Bodega()
ok_r = env_chk.recompensa(env_chk.inicio) == -1
rng_chk = np.random.default_rng(SEMILLA)
bandido(0.0, rng_chk.normal(0, 1, 5), jugadas=1, rng=rng_chk)
print("check_recompensa_inicio", ok_r)
print("check_bandido_escalar", True)
assert ok_r, "Bodega.recompensa was changed; restore the lecture class."
'''),
    ],
)
```

- [ ] **Step 4: Run helper-level check**

```bash
python - <<'PY'
from tests.notebook_ns import load_defs
ns = load_defs()
env = ns["Bodega"]()
assert env.recompensa(env.inicio) == -1
ns["bandido"](0.0, __import__("numpy").random.default_rng(2026).normal(0, 1, 5), jugadas=1,
              rng=__import__("numpy").random.default_rng(2026))
print("ok")
PY
```

Expected: `ok`

- [ ] **Step 5: Run tests**

Run: `python -m pytest tests/test_taller_celdas.py tests/test_taller_helpers.py -v`

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add tests/test_taller_celdas.py scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Add end-of-workshop check that Bodega and bandido stay intact.

EOF
)"
```

---

### Task 9: Ejecutar el cuaderno y dejar salidas

**Files:**
- Modify: `scripts/Aprendizaje_por_Refuerzo_Colab.ipynb` (outputs only; no source rewrites unless a cell errors)
- Test: run pytest + nbconvert/execute

**Interfaces:**
- Consumes: the finished notebook
- Produces: executed outputs (figures + prints) in every workshop code cell

- [ ] **Step 1: Write the failing test**

Append:

```python
def test_celdas_taller_tienen_codigo():
    nb = json.loads(NB.read_text(encoding="utf-8"))
    titles = ["### 1. Bandido", "### 2. Descuento", "### 3. Resbalón",
              "### 4. Recompensas", "### 5. Tasa de aprendizaje"]
    srcs = ["".join(c["source"]) for c in nb["cells"]]
    for t in titles:
        i = next(n for n, s in enumerate(srcs) if s.startswith(t))
        assert nb["cells"][i + 1]["cell_type"] == "code"
        assert nb["cells"][i + 2]["cell_type"] == "markdown"
        assert "".join(nb["cells"][i + 2]["source"]).startswith("**Frase.**")
```

- [ ] **Step 2: Run test**

Run: `python -m pytest tests/test_taller_celdas.py::test_celdas_taller_tienen_codigo -v`

Expected: PASS if Tasks 3–7 followed the order título → código → frase. If FAIL, reorder cells; do not skip.

- [ ] **Step 3: Execute the full notebook**

Prefer (no extra notebook deps beyond jupyter if installed):

```bash
python -m jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
```

If `jupyter` is missing, install only locally (not as a notebook dependency):

```bash
python -m pip install nbconvert ipykernel matplotlib numpy pandas
```

Then re-run the same `nbconvert` command.

Expected: exit 0. Timeout 600 s is enough for the cliff demo + 5000-episode taller jobs.

If a cell fails, fix **only** the new taller cells. Do not “fix” lecture cells unless the failure is `plt.show`/display in a headless backend (`MPLBACKEND=Agg`).

- [ ] **Step 4: Confirm outputs exist**

```bash
python - <<'PY'
import json
from pathlib import Path
nb = json.loads(Path("scripts/Aprendizaje_por_Refuerzo_Colab.ipynb").read_text())
needed = ["recompensa media =", "rutas_iguales", "n_celdas_mas_lejos",
          "len_ruta_costo_0", "mejor_alpha_estable", "check_recompensa_inicio"]
blob = []
for c in nb["cells"]:
    if c.get("cell_type") != "code":
        continue
    for o in c.get("outputs", []):
        blob.append("".join(o.get("text", [])))
        blob.append("".join(o.get("data", {}).get("text/plain", [])))
text = "\n".join(blob)
missing = [k for k in needed if k not in text]
print("missing", missing)
assert not missing, missing
PY
```

Expected: `missing []`

- [ ] **Step 5: Final pytest**

Run: `python -m pytest tests/ -v`

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/Aprendizaje_por_Refuerzo_Colab.ipynb
git commit -m "$(cat <<'EOF'
Execute the workshop notebook so each answer keeps its figure and numbers.

EOF
)"
```

If `nbconvert` wrote huge binary outputs and `git diff` is unreadable, that is expected. Do not strip outputs: the spec asks for evidence in the notebook.

---

## Self-review (plan vs spec)

| Spec | Task |
|---|---|
| Mismo archivo, no reescribir 0–18 | Tasks 1–9 only insert; `test_celda_semilla_gamma_intacta` |
| Discusión bandido Odoo | Task 1 |
| Discusión SARSA Odoo | Task 1 |
| Helpers sin parchear clase | Task 2 |
| `ε_t = 1/√t` 1-based | Task 2 tests + Task 3 |
| P1 curvas + media + last-100 | Task 3 |
| P2 γ 0.5/0.99, 5000 eps, frase honesta | Task 4 |
| P3 `iteracion_valores` + métrica Manhattan | Task 5 |
| P4 `BodegaCosto`, ruta 40 pasos | Task 6 |
| P5 α 0.01/0.1/0.9 last-300 | Task 7 |
| Una frase tras ver números | Tasks 3–7 Step 5 |
| Chequeo `recompensa` y `bandido` escalar | Task 8 |
| Ejecutar cuaderno, salidas presentes | Task 9 |
| Fuera de alcance (teoría, cliff extra, PDF) | No task |

No TBD left in helper signatures. Tasks 3–8 append cells at the end of the notebook so they never depend on the wording of a previous phrase. Each `**Frase.**` is written only after that task’s printout exists; the implementer substitutes the printed numbers before committing.
