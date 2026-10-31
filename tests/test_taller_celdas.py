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


def test_pregunta1_titulo_y_frase_con_numero():
    blob = "\n".join(cell_sources())
    assert "### 1. Bandido" in blob
    assert any(
        any(ch.isdigit() for ch in s) and ("0.5" in s or "√" in s or "sqrt" in s)
        for s in cell_sources()
        if s.startswith("**Frase.**")
    )


def test_pregunta2_titulo_y_frase():
    blob = "\n".join(cell_sources())
    assert "### 2. Descuento" in blob
    assert any(s.startswith("**Frase.**") and ("γ" in s or "gamma" in s.lower()) for s in cell_sources())


def test_pregunta3_usa_iteracion_valores():
    blob = "\n".join(cell_sources())
    assert "### 3. Resbalón" in blob
    assert "Bodega(resbalon=0.4)" in blob
    assert "iteracion_valores" in blob
    assert any(s.startswith("**Frase.**") and ("X" in s or "resbal" in s.lower()) for s in cell_sources())


def test_pregunta4_subclase_no_parche():
    blob = "\n".join(cell_sources())
    assert "### 4. Recompensas" in blob
    assert "BodegaCosto(costo_paso=0)" in blob
    assert "def recompensa(self, s2):" in blob
    assert 'return {"D": 20, "X": -20}.get(self.celda(s2), -1)' in blob
    assert any(s.startswith("**Frase.**") and ("costo" in s.lower() or "paso" in s) for s in cell_sources())


def test_pregunta5_tres_alphas():
    blob = "\n".join(cell_sources())
    assert "### 5. Tasa de aprendizaje" in blob
    assert "0.01" in blob and "0.9" in blob
    assert any(s.startswith("**Frase.**") and "α" in s for s in cell_sources())


def test_cinco_frases_y_chequeo():
    sources = cell_sources()
    frases = [s for s in sources if s.startswith("**Frase.**")]
    assert len(frases) == 5
    blob = "\n".join(sources)
    assert "check_recompensa_inicio" in blob
    assert "bandido(0.0," in blob or "bandido(0.0 ," in blob


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
