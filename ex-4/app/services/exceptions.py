class ExperimentNotFoundError(Exception):
    """Raised when an experiment is not found"""

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        super().__init__(f"Experiment {experiment_name} not found")


class ExperimentVariantWeightError(Exception):
    """Raised when an experiment variant and wheight does not match"""

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        super().__init__(
            f"Experiment {experiment_name} variants and weights do not match"
        )


class ExperimentVariantWeightTotalError(Exception):
    """Raised when an experiment sum of wheight is not 100%"""

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        super().__init__(f"Experiment {experiment_name} weight total is not 100%")
