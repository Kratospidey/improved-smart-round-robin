class Process:
    """
    Represents a single process in a scheduling algorithm.

    Attributes:
        pid (int): Process ID.
        arrival_time (int): Time at which the process arrives in the scheduling queue.
        burst_time (int): Total time required by the process to complete execution.
        remaining_time (int): Remaining execution time for the process.
        finish_time (int): Time at which the process finishes execution.
        has_started (bool): Indicates whether the process execution has started.
        stqs (list[int]): Dynamic list to store the Smart Time Quantum used at each scheduling decision for this process.
        ds (list[int]): Dynamic list to store the Delta values used at each scheduling decision for this process.
    """
    def __init__(self, pid, arrival_time, burst_time):
        """
        Initializes a new instance of the Process class.

        Args:
            pid (int): Unique identifier for the process.
            arrival_time (int): The time at which the process arrives and is ready to execute.
            burst_time (int): The total CPU time required by the process to complete execution.
        """
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.finish_time = 0
        self.has_started = False
        self.stqs = []
        self.ds = []


def calculate_stq(processes):
    """
    Calculates the Smart Time Quantum (STQ) based on average difference of adjacent RBTs.

    Args:
        ready_processes (list[Process]): A list of Process objects that are ready to execute.

    Returns:
        int: STQ.
    """
    differences = [
        abs(processes[i].remaining_time - processes[i + 1].remaining_time)
        for i in range(len(processes) - 1)
    ]
    return round(sum(differences) / len(differences)) if differences else 0


def calculate_delta(stq):
    """
    Calculates Delta as half of STQ.
    This Delta value provides flexibility to the SRR algorithm.

    Args:
        stq (int): The calculated STQ for the current round.

    Returns:
        int: Delta.
    """
    return stq // 2


def calculate_times(processes):
    """
    Calculates the average turn around and average waiting times.

    Args:
        processes (list[Process]): Processes that have finished execution.

    Returns:
        tuple: A tuple containing average turn around time and average waiting time
    """
    n = len(processes)
    total_tat = sum(process.finish_time - process.arrival_time for process in processes)
    total_wt = sum(
        (process.finish_time - process.arrival_time) - process.burst_time
        for process in processes
    )
    average_tat = total_tat / n
    average_wt = total_wt / n
    return average_tat, average_wt


def smart_round_robin(processes, print_gantt=False):
    """
    An improved implementation of the traditional round robin algorithm.
    It uses Average of Differences of RBTs for STQ and half of STQ for Delta.

    Args:
        processes (list[Process]): The list of Processes to be evaluated with Smart Round Robin Algorithm.
        print_gantt (bool, optional): If true, prints the gantt chart for the current solution. Defaults to False.

    Returns:
        tuple: It returns a tuple containing average turn around time and average waiting time.
    """
    time = 0
    gantt_chart = ""  # Initialize an empty string to build the Gantt chart
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
            if time < next_arrival_time:
                # Add idle time to the Gantt chart
                gantt_chart += f"|{time} IDLE {next_arrival_time}"
            time = next_arrival_time
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
                start_time = time  # Record the start time for this process
                process.remaining_time -= cpu_time
                time += cpu_time
                # Update the Gantt chart with the process execution
                gantt_chart += f"|{start_time} {process.pid} {time}"
                if process.remaining_time == 0:
                    process.finish_time = time

    if print_gantt:
        print(gantt_chart + "|")  # Print the final Gantt chart only if print_gantt is True
        print()
        print()
        print()

    return calculate_times(processes)
