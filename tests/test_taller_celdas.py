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
