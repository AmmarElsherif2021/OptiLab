# OptiLab — Extensible Optimization Playground

OptiLab is a lightweight, extensible toolkit for prototyping, running, and
visualizing optimization algorithms on mathematical objectives. It is designed
for researchers and engineers who want a reproducible playground: drop in an
objective function, declare variables and bounds, pick an optimizer plugin,
run experiments, and export reproducible results.

This repository is an early-stage open-source project — contributions are
welcome! OptiLab is intentionally modular: optimizers are plugins, the backend
exposes simple run APIs, and the frontend demonstrates a minimal UI for
launching experiments and inspecting results.

## Why OptiLab?

- **Fast prototyping** — run seeded demo optimizers and visualize results quickly.
- **Extensible** — add optimizers by implementing a small adapter and registering it.
- **Reproducible** — every run stores seed + configuration for exact replay.
- **Safe** — untrusted formulas should be validated and executed in isolated
  workers (future work / contributions welcome).

## Quick links

- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- License: [LICENSE](LICENSE) (MIT)
- Example PSO demo: [`backend/optimizers/pso_adapter.py`](backend/optimizers/pso_adapter.py)
- Minimal frontend: [`frontend/`](frontend) (Vite + React demo)

## Getting started (dev)

1. Clone the repo:

   ```bash
   git clone https://github.com/AmmarElsherif2021/OptiLab.git
   cd OptiLab
   ```
