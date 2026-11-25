import pytest
from deepeval.dataset import EvaluationDataset

from early_warning import get_warning

# Load the Goldens once, when the file is imported
dataset = EvaluationDataset()
dataset.add_goldens_from_json_file("data/goldens.json")


def read_risk_level(output: str) -> str:
    risk_line = next(
        line for line in output.splitlines() if line.startswith("risk_level:")
    )
    return risk_line.split(":", 1)[1].strip().lower()


@pytest.mark.parametrize("golden", dataset.goldens, ids=lambda g: g.name)
def test_risk_level_matches_golden(golden):
    output = get_warning(golden.input)
    expected = golden.additional_metadata["expected_risk_level"]

    assert read_risk_level(output) == expected, output
