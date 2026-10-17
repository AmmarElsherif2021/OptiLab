"""Optimizer plugin package.

Importing this package triggers discovery of bundled optimizer adapters so
that they register themselves with the registry on first import.
"""
from backend.optimizers import registry    # noqa: F401
from backend.optimizers import pso_adapter  # noqa: F401
