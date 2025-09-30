from app.models.experiments import ExperimentsConfig, ExperimentAssignment
from app.services.exceptions import (
    ExperimentNotFoundError,
    ExperimentVariantWeightError,
    ExperimentVariantWeightTotalError,
)
from pydantic import BaseModel
import hashlib
from hashlib import sha256


class VariantsAssignment(BaseModel):
    start: int
    end: int
    variant_name: str
    variant_weight: int


class ExperimentsMetadata(BaseModel):
    experiment_name: str
    variants: list[VariantsAssignment]


class ExperimentsSelector:
    def __init__(self, experiments_config: ExperimentsConfig):
        self.experiments: ExperimentsConfig = experiments_config
        self.experiments_metadata: dict[str, ExperimentsMetadata] = (
            self._generate_variants_metadata()
        )

    def _generate_variants_metadata(self) -> dict[str, ExperimentsMetadata]:
        experiment_metadata: dict[str, ExperimentsMetadata] = {}
        for experiment_name, experiment in self.experiments.items():
            variants_assignment: list[VariantsAssignment] = (
                self._calculate_variants_assignment(experiment)
            )
            experiment_metadata[experiment_name] = ExperimentsMetadata(
                experiment_name=experiment_name, variants=variants_assignment
            )
        return experiment_metadata

    def _calculate_variants_assignment(
        self, experiment: dict
    ) -> list[VariantsAssignment]:
        variants: list[VariantsAssignment] = []
        start = 0
        for i, weight in enumerate(experiment["weights"]):
            end = start + weight - 1  # -1 to make ranges inclusive and non-overlapping
            variants.append(
                VariantsAssignment(
                    position=i,
                    start=start,
                    end=end,
                    variant_name=experiment["variants"][i],
                    variant_weight=weight,
                )
            )
            start = end + 1
        return variants

    def _get_variant_by_hash(
        self, user_hash: sha256, experiment_name: str
    ) -> VariantsAssignment:
        experiment_metadata = self.experiments_metadata[experiment_name]
        hash_int = int(user_hash, 16)
        # get variant based on hash_int and the variant's specified weights
        variant_position = (
            hash_int % 100
        )  # this will give us a number between 0 and total_weight==100

        for variant in experiment_metadata.variants:
            if variant_position >= variant.start and variant_position <= variant.end:
                return variant
        return None

    def select_experiment(
        self, experiment_name: str, user_id: str
    ) -> ExperimentAssignment:
        """Select a variant for a user in an experiment based on hash assignment."""
        if experiment_name not in self.experiments:
            raise ExperimentNotFoundError(f"Experiment {experiment_name} not found")

        experiment = self.experiments[experiment_name]
        if len(experiment["variants"]) != len(experiment["weights"]):
            raise ExperimentVariantWeightError(experiment_name)

        total_weight = sum(experiment["weights"])
        if total_weight != 100:
            raise ExperimentVariantWeightTotalError(experiment_name)

        # get user/experiment hash
        user_hash = hashlib.sha256(f"{user_id}_{experiment_name}".encode()).hexdigest()
        variant: VariantsAssignment = self._get_variant_by_hash(
            user_hash, experiment_name
        )

        return {
            "user_id": user_id,
            "experiment_name": experiment_name,
            "variant": variant.variant_name,
        }
