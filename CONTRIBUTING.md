# Contributing to OptiLab

Thanks for your interest in contributing! This document explains how to
contribute code, documentation, and tests.

1. Create an issue first for non-trivial work to discuss the design.
2. Fork the repo and create a feature branch from `master` (or the branch
   the maintainers prefer).
3. Implement your changes, add tests (where appropriate), and update or add
   docs.
4. Open a pull request against the repository's `master` branch with a clear
   description.

## Optimizer plugin guidelines (quick)

- Place adapters under `backend/optimizers/`.
- Each optimizer must be registered with the registry decorator:

  ```python
  from backend.optimizers.registry import register_optimizer

  @register_optimizer("your_optimizer_name")
  def run_optimizer(config: dict) -> dict:
      # should return a serializable dict:
      #   { "best_position": [...], "best_value": float, "history": [...] }
      ...
