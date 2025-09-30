from pydantic import BaseModel


class Experiment(BaseModel):
    variants: list[str]
    weights: list[int]


class ExperimentsConfig(BaseModel):
    experiments: dict[str, Experiment]


class ExperimentAssignment(BaseModel):
    user_id: str
    experiment_name: str
    variant: str
