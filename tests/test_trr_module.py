import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pytest
from modules import trr_module as tm

# Define test data and expected results
test_data = [
    (6, [("P0", 0, 12), ("P1", 0, 34), ("P2", 0, 8), ("P3", 0, 19)], (51.0, 32.75)),
    (
        4,
        [("P0", 0, 2), ("P1", 0, 5), ("P2", 0, 6), ("P3", 0, 3), ("P4", 0, 9)],
        (15.6, 10.6),
    ),
    (20, [("P0", 0, 26), ("P1", 0, 67), ("P2", 0, 82), ("P3", 0, 11)], (124.5, 78.0)),
    (2, [("P0", 0, 8), ("P1", 2, 6), ("P2", 7, 11), ("P3", 0, 5)], (19.5, 12.0)),
]


@pytest.mark.parametrize("time_quantum, processes, expected", test_data)
def test_round_robin_scheduler(time_quantum, processes, expected):
    scheduler = tm.RoundRobinScheduler(time_quantum=time_quantum)
    for name, arrival, burst in processes:
        scheduler.add_process(name, arrival, burst)

    scheduler.execute()
    avg_tat, avg_wt = scheduler.calculate_averages()

    expected_avg_tat, expected_avg_wt = expected
    assert round(avg_tat, 2) == expected_avg_tat and round(avg_wt, 2) == expected_avg_wt
