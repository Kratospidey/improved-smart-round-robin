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


def calculate_stq(processes):
    differences = [
        abs(processes[i].remaining_time - processes[i + 1].remaining_time)
        for i in range(len(processes) - 1)
    ]
    return round(sum(differences) / len(differences)) if differences else 0


def calculate_delta(stq):
    return stq // 2


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
            time = next_arrival_time if next_arrival_time > time else time + 1
            continue

        # Calculate STQ and Delta based on ready processes
        ready_processes.sort(key=lambda x: x.remaining_time)
        stq = max(calculate_stq(ready_processes), 1)  # STQ should be at least 1
        delta = calculate_delta(stq)

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
                process.remaining_time -= cpu_time
                time += cpu_time
                if process.remaining_time == 0:
                    process.finish_time = time

    return calculate_times(processes)
