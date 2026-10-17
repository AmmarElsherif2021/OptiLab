from backend.optimizers.registry import register_optimizer
from backend.psoutil import run_pso_sync


@register_optimizer("pso")
def run_pso_adapter(config: dict) -> dict:
    """Adapter that maps a generic config dict onto ``psoutil.run_pso_sync``.

    Expected keys (all optional):
        iterations : int, default 100
        particles  : int, default 30
        seed       : int | None
        bounds     : [lo, hi], default (-5.12, 5.12)
        dim        : int, default 2
    """
    iterations = int(config.get("iterations", 100))
    particles  = int(config.get("particles", 30))
    seed       = config.get("seed", None)
    bounds     = tuple(config.get("bounds", (-5.12, 5.12)))
    dim        = int(config.get("dim", 2))

    return run_pso_sync(
        iterations=iterations,
        n_particles=particles,
        seed=seed,
        bounds=bounds,
        dim=dim,
    )
