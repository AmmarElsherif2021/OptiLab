from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import uuid
from typing import Any, Dict, Optional

# Importing the package triggers optimizer discovery (registers "pso", ...).
import backend.optimizers  # noqa: F401
from backend.optimizers.registry import get_optimizer, list_optimizers

app = FastAPI(title="OptiLab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RUNS: Dict[str, Dict[str, Any]] = {}


class OptimizerSpec(BaseModel):
    name: str = "pso"
    config: Dict[str, Any] = {}


class RunRequest(BaseModel):
    optimizer: OptimizerSpec
    formula: Optional[str] = None
    variables: Optional[Any] = None
    bounds: Optional[Any] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/opt/optimizers")
def optimizers():
    return {"optimizers": list_optimizers()}


@app.post("/api/opt/run")
def start_run(req: RunRequest):
    optimizer_fn = get_optimizer(req.optimizer.name)
    if optimizer_fn is None:
        raise HTTPException(
            status_code=400,
            detail=f"optimizer '{req.optimizer.name}' not found",
        )

    run_id = str(uuid.uuid4())
    RUNS[run_id] = {
        "status": "pending",
        "result": None,
        "meta": {"optimizer": req.optimizer.name},
    }

    def worker(rid: str, fn, config: dict):
        try:
            RUNS[rid]["status"] = "running"
            result = fn(config)
            RUNS[rid]["status"] = "completed"
            RUNS[rid]["result"] = result
        except Exception as exc:  # noqa: BLE001
            RUNS[rid]["status"] = "failed"
            RUNS[rid]["result"] = {"error": str(exc)}

    threading.Thread(
        target=worker,
        args=(run_id, optimizer_fn, req.optimizer.config),
        daemon=True,
    ).start()

    return {"run_id": run_id}


@app.get("/api/opt/runs/{run_id}/result")
def get_result(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail="run_id not found")
    return RUNS[run_id]
