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
