"""Particle Swarm Optimization utilities (synchronous, dependency-free).

Objective: the 2-D Rastrigin function (a standard multimodal benchmark).
"""
import math
import random
from typing import Optional, Sequence, Tuple


A = 10.0


def rastrigin(x: Sequence[float]) -> float:
    """Standard Rastrigin function; global minimum is 0 at x = (0,...,0)."""
    n = len(x)
    return A * n + sum(xi * xi - A * math.cos(2.0 * math.pi * xi) for xi in x)


def run_pso_sync(
    iterations: int = 100,
    n_particles: int = 30,
    seed: Optional[int] = None,
    bounds: Tuple[float, float] = (-5.12, 5.12),
    dim: int = 2,
    w: float = 0.7,
    c1: float = 1.5,
    c2: float = 1.5,
) -> dict:
    """Run PSO on the Rastrigin function and return a JSON-serializable result.

    Returns:
        {
          "best_position": [...],
          "best_value": float,
          "history": [{"iteration": int, "best_value": float}, ...],
          "iterations": int,
          "particles": int,
          "seed": int | None
        }
    """
    rng = random.Random(seed)
    lo, hi = bounds

    particles = []
    for _ in range(n_particles):
        pos = [rng.uniform(lo, hi) for _ in range(dim)]
        vel = [rng.uniform(-1.0, 1.0) for _ in range(dim)]
        particles.append(
            {"pos": pos, "vel": vel, "best": pos[:], "best_val": rastrigin(pos)}
        )

    gbest = min(particles, key=lambda p: p["best_val"])
    gbest_pos = gbest["best"][:]
    gbest_val = gbest["best_val"]

    history = []
    for it in range(iterations):
        for p in particles:
            for d in range(dim):
                r1, r2 = rng.random(), rng.random()
                p["vel"][d] = (
                    w * p["vel"][d]
                    + c1 * r1 * (p["best"][d] - p["pos"][d])
                    + c2 * r2 * (gbest_pos[d] - p["pos"][d])
                )
                # clamp position into bounds
                p["pos"][d] = min(hi, max(lo, p["pos"][d] + p["vel"][d]))

            val = rastrigin(p["pos"])
            if val < p["best_val"]:
                p["best_val"] = val
                p["best"] = p["pos"][:]
                if val < gbest_val:
                    gbest_val = val
                    gbest_pos = p["pos"][:]

        history.append({"iteration": it, "best_value": gbest_val})

    return {
        "best_position": gbest_pos,
        "best_value": gbest_val,
        "history": history,
        "iterations": iterations,
        "particles": n_particles,
        "seed": seed,
    }
