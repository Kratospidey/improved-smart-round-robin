import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from modules import isrr_module as im




# Define test data for the research paper cases
@pytest.fixture(
    params=[
        (
            [
                im.Process("P0", 0, 12),
                im.Process("P1", 0, 34),
                im.Process("P2", 0, 8),
                im.Process("P3", 0, 19),
            ],
            (35.00, 16.75),
        ),
        (
            [
                im.Process("P0", 0, 2),
                im.Process("P1", 0, 5),
                im.Process("P2", 0, 6),
                im.Process("P3", 0, 3),
                im.Process("P4", 0, 9),
            ],
            (11.60, 6.60),
        ),
        (
            [
                im.Process("P0", 0, 26),
                im.Process("P1", 0, 67),
                im.Process("P2", 0, 82),
                im.Process("P3", 0, 11),
            ],
            (84.50, 38.00),
        ),
        (
            [
                im.Process("P0", 0, 8),
                im.Process("P1", 2, 6),
                im.Process("P2", 7, 11),
                im.Process("P3", 0, 5),
            ],
            (14.50, 7.00),
        ),
    ]
)
def case_data(request):
    return request.param


# Test function for research paper cases
def test_research_paper_cases(case_data):
    processes, expected_values = case_data
    atat, awt = im.smart_round_robin(processes)
    expected_atat, expected_awt = expected_values
    assert (
        round(atat, 2) == expected_atat and round(awt, 2) == expected_awt
    ), f"Failed for processes: {[p.pid for p in processes]}"
