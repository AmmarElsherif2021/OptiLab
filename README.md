# Optimization Playground

General-purpose, extensible optimizer app (demo + framework). Turn the existing PSO demo into a recruiter-friendly, reproducible playground where users paste mathematical objectives, declare variables/bounds, pick optimizers, run experiments, and visualize/export results.

## Goal (short)
Turn the PSO demo into a general-purpose optimizer app where users can:
- Paste or enter a mathematical objective (formula).
- Declare variables, domains, and control parameters.
- Select an optimizer (PSO now; others later).
- Run and visualize optimization (live / step / batch).
- Save and export reproducible experiments.

## Design priorities
- Simplicity and polish — recruiter-friendly UI and demos.
- Extensibility — easy to add new optimizers (plugin-style).
- Safety and reproducibility for user-provided formulas.
- Useful for engineers & researchers (experiment management, exports, comparisons).

## Key features
- Formula editor with LaTeX/MathJax preview and variable auto-detection.
- Per-variable configuration: name, bounds, type (continuous / discrete).
- Safe formula parsing and numeric evaluation (sympy → numpy/numexpr).
- Multiple execution modes: seeded demo runs, full experiments, benchmarks.
- Live visualization (contours, particle overlays, convergence plots).
- Experiment management: save runs, download CSV/JSON, export reproducible scripts.
- Extensible optimizer registry and adapter interfaces for third-party libraries.

## Product use-cases
- Research prototyping: define custom objectives and compare optimizers reproducibly.
- Teaching & exploration: students experiment with formulas, parameters, and visualizations.
- Small experiment server: programmatic API for sweeps and batch exports.

## UX flow (what the user does)
1. Enter objective: paste a mathematical formula (e.g., `x**2 + y**2 + 10*(1 - cos(2*pi*x))`).
2. Define variables: names, dimensionality, bounds per variable, types.
3. (Optional) Add constraints (equality/inequality or simple bounds).
4. Choose optimizer & configure hyperparameters (PSO, GA, CMA-ES, ...).
5. Run: immediate seeded demo or full experiment with N trials.
6. Visualize: contour (1–2D), particle overlay, convergence; high-D projections for >2D.
7. Export/save: CSV per run, aggregated benchmark summary, reproducible metadata.
8. Extend: add new optimizer through plugin interface.

## Formula input — parsing, safety & UX
- Frontend:
  - Text input with MathJax preview and Monaco (optional).
  - Variable list UI with auto-detection and editable names/domains.
- Backend:
  - Validate/inspect formulas with sympy (sympify).
  - Convert to fast numeric functions using `sympy.lambdify` (numpy) or `numexpr`.
  - Use a safe, whitelisted namespace of functions (numpy/math only).
- Safety:
  - Reject expressions with attribute access, imports, or unsafe names.
  - Execute evaluations inside sandboxed worker processes with timeouts and resource limits.
  - Deterministic seeding + rate limits for production.

UX extras:
- Built-in templates (Rastrigin, Rosenbrock, Ackley, Sphere).
- Sample value preview and sanity checks before running an optimizer.

## Extensible optimizer architecture (recommended)
- Core Optimizer interface (Python):

  class OptimizerBase:
    def __init__(self, func, bounds, config, seed=None): ...
    def step(self) -> StepResult: ...
    def run(self, iterations, callback=None) -> Result: ...
    def state(self) -> dict: ...
    @classmethod
    def from_config(cls, config): ...

- Plugin pattern:
  - Place optimizers in `backend/optimizers/` and register them via a registry decorator.
  - Provide adapters for third-party toolkits (scipy, nevergrad, pycma, DEAP, Optuna, pygmo).
- Optimizer schema:
  - Each optimizer exposes a JSON schema describing hyperparameters for auto-generated frontend forms.

Example registry:
```python
registry = {}
def register_optimizer(name):
    def decorator(cls):
        registry[name] = cls
        return cls
    return decorator
```

## Backend API (BFF)
- POST /api/opt/run
  - payload: { formula, variables, bounds, optimizer: {name, config}, seed }
  - returns: run_id
- GET /api/opt/runs/{run_id}/stream
  - SSE or WebSocket streaming of history frames (positions + best_fitness)
- GET /api/opt/runs/{run_id}/result
  - final summary, artifacts download links
- POST /api/opt/benchmark
  - run N trials; returns summary id
- GET /api/opt/benchmarks/{id}/summary

## Visualization & dimensionality handling
- 1–2D:
  - Contour heatmap + particle overlay + best point markers (Plotly).
  - Animated replay and step controls.
- High-D (3+):
  - Pairwise 2D projections, PCA / t-SNE, parallel coordinates.
  - User-selectable projection axes or automatic projections.
- Convergence & metrics:
  - Live best fitness vs iteration.
  - Population stats: mean, std.
- Experiment comparison:
  - Overlay multiple runs (best/median/worst) and basic statistical tests (bootstrap CIs / t-tests).

## Execution model & persistence
- Backend: FastAPI + Uvicorn (BFF). Keep core optimizers in Python.
- Execution modes:
  - Interactive demo runs: inline with short timeouts.
  - Long runs / batch / benchmarks: background worker queue (Redis + RQ/Celery).
  - Worker jobs run in isolated processes (optionally containers) for untrusted formulas.
- Persistence:
  - SQLite for local/demo; Postgres for production.
  - Store artifacts (CSV, plots) on disk or S3; keep run metadata (seed, config).
- Observability:
  - Logs for runtime, iterations, completions, and errors; basic metrics for profiling.

## Suggested initial optimizers
- Population/global: PSO (present), Differential Evolution, GA, CMA-ES
- Gradient/local: Gradient Descent, Adam, L-BFGS-B, SLSQP
- Model-based: Bayesian Optimization (skopt / optuna)
- Other: Simulated Annealing, Nelder–Mead, Powell
- Multi-objective: NSGA-II (DEAP / pygmo)
- Toolkits to integrate later: nevergrad, pygmo, optuna

## Reproducibility & experiment management
- Always store seed and full run config in metadata.
- Export a reproducible Python script to re-run experiments locally.
- Support bundling experiments (config + CSV + plots + logs) as a zip for sharing.

## Security & sandboxing
- Parse with sympy and whitelist functions only.
- Execute untrusted evaluations in worker processes with OS-level resource limits or ephemeral containers.
- Enforce timeouts and per-user quotas.

## Minimal recommended tech stack
- Frontend: React + TypeScript + Vite + Plotly + Monaco + Tailwind
- Backend: FastAPI + Uvicorn + Pydantic
- Python libs: numpy, scipy, sympy, pandas, pycma, DEAP, scikit-optimize / optuna
- Queue/workers: Redis + RQ or Celery
- DB: SQLite (local) / Postgres (prod)
- Storage: local FS or S3
- CI: GitHub Actions
- Container: Docker + docker-compose

## Suggested roadmap (example)
- Week 0: PSO refactor, tests, register PSO in registry.
- Week 1: FastAPI endpoints, safe formula parsing, seeded demo endpoint, basic React UI.
- Week 2: SSE streaming, run/export, experiment metadata storage.
- Week 3: Background job queue, add DE and CMA-ES adapters, run comparison UI.
- Week 4: Add gradient-based optimizers, projection visualizations.
- Weeks 5+: Bayesian opt, NSGA-II, plugin docs, auth & deployment polish.

## Getting started (local / demo)
1. Clone the repo
2. Create a Python venv and install dependencies:
   - numpy, scipy, sympy, pandas, pycma, fastapi, uvicorn, plotly, redis, rq (as needed)
3. Start the backend:
   - uvicorn backend.main:app --reload
4. Start the frontend (if included):
   - cd frontend && npm install && npm run dev
5. Open the UI, pick a template objective (Rastrigin), and run the seeded demo.

## Contributing
- Add new optimizers under `backend/optimizers` and register them.
- Add unit tests for optimizer correctness and reproducibility.
- Keep formula parsing strict and safe; follow the sandboxing patterns in `backend/safety/*`.

## License
Specify a license (e.g., MIT). Add `LICENSE` file to the repo.
