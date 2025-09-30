from fastapi import FastAPI
from app.services.experiments_selector import ExperimentsSelector
from app.models.experiments import ExperimentAssignment, ExperimentsConfig
import json
import logging
import pathlib
from fastapi import HTTPException
from app.services.exceptions import (
    ExperimentNotFoundError,
    ExperimentVariantWeightError,
    ExperimentVariantWeightTotalError,
)

app = FastAPI(
    title="Experiment Assignment API",
    description="API for assigning experiments to users",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
try:
    BASE_DIR = pathlib.Path(__file__).parent
    EXPERIMENTS_CONFIG_PATH = f"{BASE_DIR}/data/experiments.json"
    experiments = {}
    with open(EXPERIMENTS_CONFIG_PATH, "r", encoding="utf-8") as f:
        experiments = json.load(f)
except FileNotFoundError as exc:
    logging.error("Experiments config file not found at %s", EXPERIMENTS_CONFIG_PATH)
    raise FileNotFoundError(
        f"Experiments config file not found at {EXPERIMENTS_CONFIG_PATH}"
    ) from exc


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "experiment-assignment-api"}


@app.get("/assign", response_model=ExperimentAssignment)
def assign(experiment_name: str, user_id: str) -> ExperimentAssignment:
    try:
        experiments_selector = ExperimentsSelector(experiments)
        result = experiments_selector.select_experiment(experiment_name, user_id)
        return result
    except ExperimentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ExperimentVariantWeightError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ExperimentVariantWeightTotalError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
