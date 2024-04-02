import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from modules import srr_module as sm


# Define test data for the research paper cases
@pytest.fixture(
    params=[
        (
            [
                sm.Process("P0", 0, 12),
                sm.Process("P1", 0, 34),
                sm.Process("P2", 0, 8),
                sm.Process("P3", 0, 19),
            ],
            (37.25, 19),
        ),
        (
            [
                sm.Process("P0", 0, 2),
                sm.Process("P1", 0, 5),
                sm.Process("P2", 0, 6),
                sm.Process("P3", 0, 3),
                sm.Process("P4", 0, 9),
            ],
            (13.2, 8.2),
        ),
        (
            [
                sm.Process("P0", 0, 26),
                sm.Process("P1", 0, 67),
                sm.Process("P2", 0, 82),
                sm.Process("P3", 0, 11),
            ],
            (98, 51.5),
        ),
        (
            [
                sm.Process("P0", 0, 8),
                sm.Process("P1", 2, 6),
                sm.Process("P2", 7, 11),
                sm.Process("P3", 0, 5),
            ],
            (15.75, 8.25),
        ),
    ]
)
def case_data(request):
    return request.param


# Test function for research paper cases
def test_research_paper_cases(case_data):
    processes, expected_values = case_data
    atat, awt = sm.smart_round_robin(processes)
    expected_atat, expected_awt = expected_values
    assert (
        round(atat, 2) == expected_atat and round(awt, 2) == expected_awt
    ), f"Failed for processes: {[p.pid for p in processes]}"
