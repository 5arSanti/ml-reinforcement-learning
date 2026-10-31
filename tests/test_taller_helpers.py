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
