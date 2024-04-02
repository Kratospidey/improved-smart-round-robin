class RoundRobinScheduler:
    def __init__(self, time_quantum):
        self.time_quantum = time_quantum
        self.processes = []

    def add_process(self, name, arrival_time, burst_time):
        self.processes.append(
            {
                "name": name,
                "arrival_time": arrival_time,
                "burst_time": burst_time,
                "remaining_time": burst_time,
                "start_time": None,  # Track the first time a process starts
                "completion_time": 0,
            }
        )
        self.processes.sort(key=lambda x: x["arrival_time"])  # Sort by arrival time

    def execute(self):
        current_time = 0
        ready_queue = []
        completed_processes = 0
        n = len(self.processes)

        while completed_processes < n:
            # Add newly arrived processes to the ready queue
            for process in self.processes:
                if (
                    process["arrival_time"] <= current_time
                    and process not in ready_queue
                    and process["remaining_time"] > 0
                ):
                    ready_queue.append(process)

            if ready_queue:
                process = ready_queue.pop(0)
                if process["start_time"] is None:
                    process["start_time"] = current_time

                if process["remaining_time"] > self.time_quantum:
                    current_time += self.time_quantum
                    process["remaining_time"] -= self.time_quantum
                else:
                    current_time += process["remaining_time"]
                    process["remaining_time"] = 0
                    process["completion_time"] = current_time
                    completed_processes += 1

                # Re-add the process to the end of the queue if it's not finished
                if process["remaining_time"] > 0:
                    ready_queue.append(process)
            else:
                # Find the next process arrival time if the ready queue is empty
                next_arrival_time = min(
                    [
                        p["arrival_time"]
                        for p in self.processes
                        if p["arrival_time"] > current_time
                    ],
                    default=current_time,
                )
                current_time = max(
                    current_time + 1, next_arrival_time
                )  # Increment current time to the next process arrival time or by 1

    def calculate_averages(self):
        total_tat = 0
        total_wt = 0

        for process in self.processes:
            tat = process["completion_time"] - process["arrival_time"]
            wt = tat - process["burst_time"]
            total_tat += tat
            total_wt += wt

        avg_tat = total_tat / len(self.processes)
        avg_wt = total_wt / len(self.processes)
        return avg_tat, avg_wt


# Test cases

# Test Case 1
scheduler1 = RoundRobinScheduler(time_quantum=6)
processes_case1 = [("P0", 0, 12), ("P1", 0, 34), ("P2", 0, 8), ("P3", 0, 19)]
for name, arrival, burst in processes_case1:
    scheduler1.add_process(name, arrival, burst)

scheduler1.execute()
avg_tat_1, avg_wt_1 = scheduler1.calculate_averages()
print(f"Case I - Avg TAT: {avg_tat_1}, Avg WT: {avg_wt_1}")

# Test Case 2
scheduler2 = RoundRobinScheduler(time_quantum=4)
processes_case2 = [("P0", 0, 2), ("P1", 0, 5), ("P2", 0, 6), ("P3", 0, 3), ("P4", 0, 9)]
for name, arrival, burst in processes_case2:
    scheduler2.add_process(name, arrival, burst)

scheduler2.execute()
avg_tat_2, avg_wt_2 = scheduler2.calculate_averages()
print(f"Case II - Avg TAT: {avg_tat_2}, Avg WT: {avg_wt_2}")

# Test Case 3
scheduler3 = RoundRobinScheduler(time_quantum=20)
processes_case3 = [("P0", 0, 26), ("P1", 0, 67), ("P2", 0, 82), ("P3", 0, 11)]
for name, arrival, burst in processes_case3:
    scheduler3.add_process(name, arrival, burst)

scheduler3.execute()
avg_tat_3, avg_wt_3 = scheduler3.calculate_averages()
print(f"Case III - Avg TAT: {avg_tat_3}, Avg WT: {avg_wt_3}")

# Test Case 4
scheduler4 = RoundRobinScheduler(time_quantum=2)
processes_case4 = [("P0", 0, 8), ("P1", 2, 6), ("P2", 7, 11), ("P3", 0, 5)]
for name, arrival, burst in processes_case4:
    scheduler4.add_process(name, arrival, burst)

scheduler4.execute()
avg_tat_4, avg_wt_4 = scheduler4.calculate_averages()
print(f"Case IV - Avg TAT: {avg_tat_4}, Avg WT: {avg_wt_4}")
