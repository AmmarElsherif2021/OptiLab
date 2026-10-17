# Minimal optimizer registry for plugin adapters.
from typing import Callable, Dict

registry: Dict[str, Callable[[dict], dict]] = {}


def register_optimizer(name: str):
    """Decorator that registers a callable under ``name``."""
    def decorator(fn: Callable[[dict], dict]) -> Callable[[dict], dict]:
        if name in registry:
            raise ValueError(f"optimizer '{name}' already registered")
        registry[name] = fn
        return fn
    return decorator


def get_optimizer(name: str):
    return registry.get(name)


def list_optimizers():
    return sorted(registry.keys())
