from math import sqrt, floor


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.finish_time = 0
        self.has_started = False
        self.stqs = []
        self.ds = []


def calculate_stq_delta(ready_processes):
    burst_times = [p.remaining_time for p in ready_processes]
    average_bt = sum(burst_times) / len(burst_times) if burst_times else 0
    stq = max(1, round(average_bt))  # Ensure STQ is at least 1

    differences = [
        abs(ready_processes[i].remaining_time - ready_processes[i + 1].remaining_time)
        for i in range(len(ready_processes) - 1)
    ]
    delta = max(
        1, round(sum(differences) / len(differences)) if differences else 0
    )  # Ensure delta is at least 1
    return stq, delta


def calculate_times(processes):
    n = len(processes)
    total_tat = sum(process.finish_time - process.arrival_time for process in processes)
    total_wt = sum(
        (process.finish_time - process.arrival_time) - process.burst_time
        for process in processes
    )
    average_tat = total_tat / n
    average_wt = total_wt / n
    return average_tat, average_wt


def smart_round_robin(processes):
    time = 0
    gantt_chart = ""  # Initialize the Gantt chart string
    while any(p.remaining_time > 0 for p in processes):
        # Filter processes that have arrived and have remaining time
        ready_processes = [
            p for p in processes if p.remaining_time > 0 and p.arrival_time <= time
        ]

        # If no processes are ready, increment time to the next process arrival
        if not ready_processes:
            next_arrival_time = min(
                p.arrival_time
                for p in processes
                if p.remaining_time > 0 and p.arrival_time > time
            )
            # Add idle time to the Gantt chart if there is a gap
            if time < next_arrival_time:
                gantt_chart += f"|{time} IDLE {next_arrival_time}"
            time = next_arrival_time
            continue

        # Calculate STQ and Delta based on ready processes
        ready_processes.sort(key=lambda x: x.remaining_time)
        stq, delta = calculate_stq_delta(ready_processes)

        for process in ready_processes:
            process.stqs.append(stq)
            process.ds.append(delta)
            if process.remaining_time > 0:
                # Determine the time to assign to the CPU
                cpu_time = (
                    process.remaining_time
                    if process.remaining_time <= stq + delta
                    else stq
                )
                start_time = time  # Record the start time for this process
                process.remaining_time -= cpu_time
                time += cpu_time
                # Update the Gantt chart with the process execution
                gantt_chart += f"|{start_time} {process.pid} {time}"
                if process.remaining_time == 0:
                    process.finish_time = time

    print(gantt_chart + "|")  # Print the final Gantt chart
    print()
    print()
    print()

    return calculate_times(processes)


# Test cases
# Format is Process(PID, AT, BT)
cases = [
    # Research Paper Cases
    [
        Process("P0", 0, 12),
        Process("P1", 0, 34),
        Process("P2", 0, 8),
        Process("P3", 0, 19),
    ],
    [
        Process("P0", 0, 2),
        Process("P1", 0, 5),
        Process("P2", 0, 6),
        Process("P3", 0, 3),
        Process("P4", 0, 9),
    ],
    [
        Process("P0", 0, 26),
        Process("P1", 0, 67),
        Process("P2", 0, 82),
        Process("P3", 0, 11),
    ],
    [
        Process("P0", 0, 8),
        Process("P1", 2, 6),
        Process("P2", 7, 11),
        Process("P3", 0, 5),
    ],
    # Class problems
    [
        Process("P1", 0, 4),
        Process("P2", 1, 5),
        Process("P3", 2, 2),
        Process("P4", 3, 1),
        Process("P5", 4, 6),
        Process("P6", 6, 3),
    ],
    [
        Process("P1", 5, 5),
        Process("P2", 4, 6),
        Process("P3", 3, 7),
        Process("P4", 1, 9),
        Process("P5", 2, 2),
        Process("P6", 6, 3),
    ],
    # Random Test Cases
    # Small number of processes, small burst times, same ATs
    [Process("P1", 0, 4), Process("P2", 0, 5), Process("P3", 0, 3)],
    # Small number of processes, large burst times, same ATs
    [Process("P1", 0, 40), Process("P2", 0, 50), Process("P3", 0, 30)],
    # Small number of processes, small burst times, small diff in ATs
    [Process("P1", 1, 4), Process("P2", 2, 5), Process("P3", 3, 3)],
    # Small number of processes, small burst times, large diff in ATs
    [Process("P1", 1, 4), Process("P2", 10, 5), Process("P3", 20, 3)],
    # Large number of processes, small burst times, same ATs
    [
        Process("P1", 0, 3),
        Process("P2", 0, 4),
        Process("P3", 0, 2),
        Process("P4", 0, 5),
        Process("P5", 0, 3),
        Process("P6", 0, 2),
        Process("P7", 0, 1),
    ],
    # Large number of processes, large burst times, same ATs
    [
        Process("P1", 0, 30),
        Process("P2", 0, 40),
        Process("P3", 0, 20),
        Process("P4", 0, 50),
        Process("P5", 0, 30),
        Process("P6", 0, 20),
        Process("P7", 0, 10),
    ],
    # Large number of processes, small burst times, small diff in ATs
    [
        Process("P1", 1, 3),
        Process("P2", 2, 4),
        Process("P3", 3, 2),
        Process("P4", 4, 5),
        Process("P5", 5, 3),
        Process("P6", 6, 2),
        Process("P7", 7, 1),
    ],
    # Large number of processes, small burst times, large diff in ATs
    [
        Process("P1", 1, 3),
        Process("P2", 10, 4),
        Process("P3", 20, 2),
        Process("P4", 30, 5),
        Process("P5", 40, 3),
        Process("P6", 50, 2),
        Process("P7", 60, 1),
    ],
    # Mix of small and large burst times with varied ATs
    [
        Process("P1", 0, 10),
        Process("P2", 2, 20),
        Process("P3", 4, 5),
        Process("P4", 6, 15),
        Process("P5", 8, 10),
        Process("P6", 10, 5),
        Process("P7", 12, 20),
    ],
]

averages = []

for case in cases:
    averages.append(smart_round_robin(case))

# ! prints the stq & delta value for each round for each process, used for debugging
for process in cases[1]:
    print(f"{process.pid}:")

    rounds_delta = [f"Round {i + 1}: {delta}" for i, delta in enumerate(process.ds)]
    rounds_stq = [f"Round {i + 1}: {stq}" for i, stq in enumerate(process.stqs)]
    print(rounds_stq)
    print(rounds_delta)


expected_research_values = [(37.25, 19), (13.2, 8.2), (98, 51.5), (15.75, 8.25)]

expected_class_values = [
    # These were calculated in class
    (10.833, 7.333),
    (21.33, 16.00),
]

research_cases_results = averages[:4]
class_problem_results = averages[4:6]
random_cases_results = averages[6:]


# Display the results of Research Paper Cases
print(f"\033[91mResearch Paper Cases:\033[0m")
for i, (atat, awt) in enumerate(research_cases_results, start=1):
    print()
    print(f"\033[92mCase {i}:\033[0m")
    print(
        f"Case {i}: Expected Turnaround Time (TAT): {expected_research_values[i-1][0]}, Expected Waiting Time (WT): {expected_research_values[i-1][1]}"
    )
    print()
    print(
        f"Case {i}: Average Turnaround Time (ATAT) = {atat:.2f}, Average Waiting Time (AWT) = {awt:.2f}"
    )
    print(
        "-----------------------------------------------------------------------------------------------------------------"
    )


print()
print()
print()
# Display the results of Class Problems
print(f"\033[91mClass Problems:\033[0m")
for i, (atat, awt) in enumerate(class_problem_results, start=1):
    print()
    print(f"\033[92mCase {i}:\033[0m")
    print(
        f"Case {i}: Expected Turnaround Time (TAT): {expected_class_values[i-1][0]}, Expected Waiting Time (WT): {expected_class_values[i-1][1]}"
    )
    print()
    print(
        f"Case {i}: Average Turnaround Time (ATAT) = {atat:.2f}, Average Waiting Time (AWT) = {awt:.2f}"
    )
    print(
        "-----------------------------------------------------------------------------------------------------------------"
    )

if random_cases_results:
    print()
    print()
    print()
    # Display the results of Random Test Cases
    print(f"\033[91mRandom Test Cases:\033[0m")
    for i, (atat, awt) in enumerate(random_cases_results, start=1):
        print()
        print(
            f"Case {i}: Average Turnaround Time (ATAT) = {atat:.2f}, Average Waiting Time (AWT) = {awt:.2f}"
        )
        print(
            "-----------------------------------------------------------------------------------------------------------------"
        )
