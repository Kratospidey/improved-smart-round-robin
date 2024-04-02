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
