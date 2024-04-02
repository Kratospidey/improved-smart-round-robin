import trr_module as tm

# Test cases

# Test Case 1
scheduler1 = tm.RoundRobinScheduler(time_quantum=6)
processes_case1 = [("P0", 0, 12), ("P1", 0, 34), ("P2", 0, 8), ("P3", 0, 19)]
for name, arrival, burst in processes_case1:
    scheduler1.add_process(name, arrival, burst)

scheduler1.execute()
avg_tat_1, avg_wt_1 = scheduler1.calculate_averages()
print(f"Case I - Avg TAT: {avg_tat_1}, Avg WT: {avg_wt_1}")

# Test Case 2
scheduler2 = tm.RoundRobinScheduler(time_quantum=4)
processes_case2 = [("P0", 0, 2), ("P1", 0, 5), ("P2", 0, 6), ("P3", 0, 3), ("P4", 0, 9)]
for name, arrival, burst in processes_case2:
    scheduler2.add_process(name, arrival, burst)

scheduler2.execute()
avg_tat_2, avg_wt_2 = scheduler2.calculate_averages()
print(f"Case II - Avg TAT: {avg_tat_2}, Avg WT: {avg_wt_2}")

# Test Case 3
scheduler3 = tm.RoundRobinScheduler(time_quantum=20)
processes_case3 = [("P0", 0, 26), ("P1", 0, 67), ("P2", 0, 82), ("P3", 0, 11)]
for name, arrival, burst in processes_case3:
    scheduler3.add_process(name, arrival, burst)

scheduler3.execute()
avg_tat_3, avg_wt_3 = scheduler3.calculate_averages()
print(f"Case III - Avg TAT: {avg_tat_3}, Avg WT: {avg_wt_3}")

# Test Case 4
scheduler4 = tm.RoundRobinScheduler(time_quantum=2)
processes_case4 = [("P0", 0, 8), ("P1", 2, 6), ("P2", 7, 11), ("P3", 0, 5)]
for name, arrival, burst in processes_case4:
    scheduler4.add_process(name, arrival, burst)

scheduler4.execute()
avg_tat_4, avg_wt_4 = scheduler4.calculate_averages()
print(f"Case IV - Avg TAT: {avg_tat_4}, Avg WT: {avg_wt_4}")
