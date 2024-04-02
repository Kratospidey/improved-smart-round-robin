import srr_module as sm

# Test cases
# Format is Process(PID, AT, BT)
cases = [
    # Research Paper Cases
    [
        sm.Process("P0", 0, 12),
        sm.Process("P1", 0, 34),
        sm.Process("P2", 0, 8),
        sm.Process("P3", 0, 19),
    ],
    [
        sm.Process("P0", 0, 2),
        sm.Process("P1", 0, 5),
        sm.Process("P2", 0, 6),
        sm.Process("P3", 0, 3),
        sm.Process("P4", 0, 9),
    ],
    [
        sm.Process("P0", 0, 26),
        sm.Process("P1", 0, 67),
        sm.Process("P2", 0, 82),
        sm.Process("P3", 0, 11),
    ],
    [
        sm.Process("P0", 0, 8),
        sm.Process("P1", 2, 6),
        sm.Process("P2", 7, 11),
        sm.Process("P3", 0, 5),
    ],
    # Class problems
    [
        sm.Process("P1", 0, 4),
        sm.Process("P2", 1, 5),
        sm.Process("P3", 2, 2),
        sm.Process("P4", 3, 1),
        sm.Process("P5", 4, 6),
        sm.Process("P6", 6, 3),
    ],
    [
        sm.Process("P1", 5, 5),
        sm.Process("P2", 4, 6),
        sm.Process("P3", 3, 7),
        sm.Process("P4", 1, 9),
        sm.Process("P5", 2, 2),
        sm.Process("P6", 6, 3),
    ],
    # Random Test Cases
    # 1. Small number of processes, small burst times, same ATs
    [sm.Process("P1", 0, 4), sm.Process("P2", 0, 5), sm.Process("P3", 0, 3)],
    # 2. Small number of processes, large burst times, same ATs
    [sm.Process("P1", 0, 40), sm.Process("P2", 0, 50), sm.Process("P3", 0, 30)],
    # 3. Small number of processes, small burst times, small diff in ATs
    [sm.Process("P1", 1, 4), sm.Process("P2", 2, 5), sm.Process("P3", 3, 3)],
    # 4. Small number of processes, small burst times, large diff in ATs
    [sm.Process("P1", 1, 4), sm.Process("P2", 10, 5), sm.Process("P3", 20, 3)],
    # 5. Large number of processes, small burst times, same ATs
    [
        sm.Process("P1", 0, 3),
        sm.Process("P2", 0, 4),
        sm.Process("P3", 0, 2),
        sm.Process("P4", 0, 5),
        sm.Process("P5", 0, 3),
        sm.Process("P6", 0, 2),
        sm.Process("P7", 0, 1),
    ],
    # 6. Large number of processes, large burst times, same ATs
    [
        sm.Process("P1", 0, 30),
        sm.Process("P2", 0, 40),
        sm.Process("P3", 0, 20),
        sm.Process("P4", 0, 50),
        sm.Process("P5", 0, 30),
        sm.Process("P6", 0, 20),
        sm.Process("P7", 0, 10),
    ],
    # 7. Large number of processes, small burst times, small diff in ATs
    [
        sm.Process("P1", 1, 3),
        sm.Process("P2", 2, 4),
        sm.Process("P3", 3, 2),
        sm.Process("P4", 4, 5),
        sm.Process("P5", 5, 3),
        sm.Process("P6", 6, 2),
        sm.Process("P7", 7, 1),
    ],
    # 8. Large number of processes, small burst times, large diff in ATs
    [
        sm.Process("P1", 1, 3),
        sm.Process("P2", 10, 4),
        sm.Process("P3", 20, 2),
        sm.Process("P4", 30, 5),
        sm.Process("P5", 40, 3),
        sm.Process("P6", 50, 2),
        sm.Process("P7", 60, 1),
    ],
    # 9. Mix of small and large burst times with varied ATs
    [
        sm.Process("P1", 0, 10),
        sm.Process("P2", 2, 20),
        sm.Process("P3", 4, 5),
        sm.Process("P4", 6, 15),
        sm.Process("P5", 8, 10),
        sm.Process("P6", 10, 5),
        sm.Process("P7", 12, 20),
    ],
]

averages = []

for case in cases:
    averages.append(sm.smart_round_robin(case))

# ! prints the stq & delta value for each round for each process, used for debugging
# for process in cases[2]:
#     print(f"{process.pid}:")

#     rounds_delta = [f"Round {i + 1}: {delta}" for i, delta in enumerate(process.ds)]
#     rounds_stq = [f"Round {i + 1}: {stq}" for i, stq in enumerate(process.stqs)]
#     print(rounds_stq)
#     print(rounds_delta)


expected_research_values = [(37.25, 19), (13.2, 8.2), (98, 51.5), (15.75, 8.25)]

expected_class_values = [
    # These were calculated in class
    (10.833, 7.333),
    (21.33, 16.00),
]

research_cases_results = averages[:4]
class_problem_results = averages[4:6]
random_cases_results = averages[6:]

# ! uncomment out below other stuff later

# # Display the results of Research Paper Cases
# print(f"\033[91mResearch Paper Cases:\033[0m")
# for i, (atat, awt) in enumerate(research_cases_results, start=1):
#     print()
#     print(f"\033[92mCase {i}:\033[0m")
#     print(
#         f"Case {i}: Expected Turnaround Time (TAT): {expected_research_values[i-1][0]}, Expected Waiting Time (WT): {expected_research_values[i-1][1]}"
#     )
#     print()
#     print(
#         f"Case {i}: Average Turnaround Time (ATAT) = {atat:.2f}, Average Waiting Time (AWT) = {awt:.2f}"
#     )
#     print(
#         "-----------------------------------------------------------------------------------------------------------------"
#     )

# print()
# print()
# print()
# # Display the results of Class Problems
# print(f"\033[91mClass Problems:\033[0m")
# for i, (atat, awt) in enumerate(class_problem_results, start=1):
#     print()
#     print(f"\033[92mCase {i}:\033[0m")
#     print(
#         f"Case {i}: Expected Turnaround Time (TAT): {expected_class_values[i-1][0]}, Expected Waiting Time (WT): {expected_class_values[i-1][1]}"
#     )
#     print()
#     print(
#         f"Case {i}: Average Turnaround Time (ATAT) = {atat:.2f}, Average Waiting Time (AWT) = {awt:.2f}"
#     )
#     print(
#         "-----------------------------------------------------------------------------------------------------------------"
#     )

# if random_cases_results:
#     print()
#     print()
#     print()
#     # Display the results of Random Test Cases
#     print(f"\033[91mRandom Test Cases:\033[0m")
#     for i, (atat, awt) in enumerate(random_cases_results, start=1):
#         print()
#         print(
#             f"Case {i}: Average Turnaround Time (ATAT) = {atat:.2f}, Average Waiting Time (AWT) = {awt:.2f}"
#         )
#         print(
#             "-----------------------------------------------------------------------------------------------------------------"
#         )
