"""Smoke tests for the PSO optimizer adapter."""
from backend.optimizers.registry import get_optimizer, list_optimizers
from backend.optimizers.pso_adapter import run_pso_adapter


def test_pso_is_registered():
    assert "pso" in list_optimizers()
    assert get_optimizer("pso") is not None


def test_pso_smoke():
    res = run_pso_adapter({"iterations": 30, "particles": 15, "seed": 1})
    assert set(res) >= {"best_position", "best_value", "history"}
    assert len(res["best_position"]) == 2
    assert isinstance(res["best_value"], float)
    # Rastrigin is multimodal but with 15 particles x 30 iters the best value
    # should comfortably beat a random draw.
    assert res["best_value"] < 20.0
    assert len(res["history"]) == 30


def test_pso_is_reproducible_with_seed():
    a = run_pso_adapter({"iterations": 10, "particles": 8, "seed": 7})
    b = run_pso_adapter({"iterations": 10, "particles": 8, "seed": 7})
    assert a["best_position"] == b["best_position"]
    assert a["best_value"] == b["best_value"]
