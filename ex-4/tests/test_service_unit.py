import pytest
from app.services.experiments_selector import ExperimentsSelector
from collections import Counter


@pytest.fixture
def experiments_selector():
    experiments = {
        "new-signup-flow": {
            "variants": ["control", "new-design"],
            "weights": [50, 50],
        }
    }

    return ExperimentsSelector(experiments_config=experiments)


class TestAcceptanceCriteria:

    def test_ac1(self, experiments_selector):
        user_id = "1"
        experiment_name = "new-signup-flow"
        variant_1 = experiments_selector.select_experiment(
            experiment_name=experiment_name, user_id=user_id
        )
        assert variant_1["user_id"] == user_id
        assert variant_1["experiment_name"] == experiment_name

        variant_2 = experiments_selector.select_experiment(
            experiment_name=experiment_name, user_id=user_id
        )
        assert variant_2["user_id"] == user_id
        assert variant_2["experiment_name"] == experiment_name

        assert variant_1["variant"] == variant_2["variant"]

    def test_ac2(self, experiments_selector):
        user_id = "1"
        experiment_name = "not-existing-experiment"

        with pytest.raises(Exception) as exc_info:
            experiments_selector.select_experiment(
                experiment_name=experiment_name, user_id=user_id
            )

        assert "ExperimentNotFoundError" in str(type(exc_info.value))

    def test_ac3(self, experiments_selector):
        """Test that distribution of assignments approximates the configured weights"""

        # Test with a large number of unique users
        num_users = 1000
        user_ids = [f"user_{i}" for i in range(num_users)]
        experiment_name = "new-signup-flow"

        # Collect all assignments
        assignments = []
        for user_id in user_ids:
            result = experiments_selector.select_experiment(
                experiment_name=experiment_name, user_id=user_id
            )
            assignments.append(result["variant"])

        # Count the distribution
        distribution = Counter(assignments)

        # Calculate percentages
        total = len(assignments)
        control_percentage = (distribution["control"] / total) * 100
        new_design_percentage = (distribution["new-design"] / total) * 100

        # Expected percentages based on weights [50, 50]
        expected_control = 50.0
        expected_new_design = 50.0

        # Allow for some variance (±5%)
        tolerance = 5.0

        assert (
            abs(control_percentage - expected_control) <= tolerance
        ), f"Control distribution {control_percentage}% not within tolerance of {expected_control}%"
        assert (
            abs(new_design_percentage - expected_new_design) <= tolerance
        ), f"New design distribution {new_design_percentage}% not within tolerance of {expected_new_design}%"

        # Verify we got both variants (not all one variant)
        assert len(distribution) == 2, "Should have both variants assigned"
        assert "control" in distribution, "Should have control variant"
        assert "new-design" in distribution, "Should have new-design variant"
