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
