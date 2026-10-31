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
