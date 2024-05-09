import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

# Dummy results for TRR, SRR, and ISRR
trr_results = [(51.0, 32.75), (124.5, 78.0), (19.5, 12.0)]
srr_results = [(37.25, 19.00), (98.00, 51.50), (15.75, 8.25)]
isrr_results = [(35.00, 16.75), (84.50, 38.00), (14.50, 7.00)]

# Time quantums for TRR cases
time_quantums = [6, 20, 2]

# Ensure the results directory exists
results_dir = "../results/TRR_vs_SRR_vs_ISRR"
if os.path.isdir(results_dir):
    shutil.rmtree(results_dir)
os.makedirs(results_dir, exist_ok=True)


def save_comparative_plot(case_number, trr, srr, isrr, time_quantum, results_dir):
    labels = ["Average Turnaround time", "Average Waiting Time"]
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))  # Adjusting figure size
    ax.bar(x - width, trr, width, label=f"TRR (Q={time_quantum})", color="#4472C4")
    ax.bar(x, srr, width, label="SRR", color="#ED7D31")
    ax.bar(x + width, isrr, width, label="ISRR", color="#A5A5A5")

    ax.set_ylabel("Time")
    ax.set_title(f"Case {case_number} Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.savefig(os.path.join(results_dir, f"Case_{case_number}_comparison.png"))
    plt.close(fig)


for i, ((trr_tat, trr_wt), (srr_tat, srr_wt), (isrr_tat, isrr_wt), tq) in enumerate(
    zip(trr_results, srr_results, isrr_results, time_quantums), start=1
):
    save_comparative_plot(
        i, [trr_tat, trr_wt], [srr_tat, srr_wt], [isrr_tat, isrr_wt], tq, results_dir
    )


def calculate_reduction(trr, val):
    return ((trr - val) / trr) * 100


# Calculate reductions for ATAT and AWT from TRR to SRR and ISRR
atat_reductions_srr = [
    calculate_reduction(trr[0], srr[0]) for trr, srr in zip(trr_results, srr_results)
]
atat_reductions_isrr = [
    calculate_reduction(trr[0], isrr[0]) for trr, isrr in zip(trr_results, isrr_results)
]
awt_reductions_srr = [
    calculate_reduction(trr[1], srr[1]) for trr, srr in zip(trr_results, srr_results)
]
awt_reductions_isrr = [
    calculate_reduction(trr[1], isrr[1]) for trr, isrr in zip(trr_results, isrr_results)
]


def save_reduction_plot(reductions1, reductions2, labels, title, filename, results_dir):
    plt.figure(figsize=(10, 6))  # Larger figure size
    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    width = 0.35
    rects1 = ax.bar(
        x - width / 2, reductions1, width, label="TRR to SRR", color="#4472C4"
    )
    rects2 = ax.bar(
        x + width / 2, reductions2, width, label="TRR to ISRR", color="#ED7D31"
    )

    ax.set_ylabel("Reduction (%)")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Annotate bars with percentage values
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height:.2f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,  # Increasing font size
            )

    add_labels(rects1)
    add_labels(rects2)

    fig.savefig(os.path.join(results_dir, filename))
    plt.close(fig)


# Save the two separate reduction plots
save_reduction_plot(
    atat_reductions_srr,
    atat_reductions_isrr,
    ["Case I", "Case II", "Case III"],
    "ATAT Reduction Comparison",
    "Reduction_ATAT.png",
    results_dir,
)

save_reduction_plot(
    awt_reductions_srr,
    awt_reductions_isrr,
    ["Case I", "Case II", "Case III"],
    "AWT Reduction Comparison",
    "Reduction_AWT.png",
    results_dir,
)

# Context switches for ISRR and SRR
isrr_context_switches = [3, 3, 3]
srr_context_switches = [5, 9, 7]

def save_context_switch_comparison_plot(isrr_data, srr_data, labels, title, filename, results_dir):
    plt.figure(figsize=(8, 5))  # Matching the previous figure sizes
    fig, ax = plt.subplots()
    x = np.arange(len(labels))
    width = 0.35
    rects1 = ax.bar(x - width / 2, isrr_data, width, label="ISRR", color="#A5A5A5")
    rects2 = ax.bar(x + width / 2, srr_data, width, label="SRR", color="#ED7D31")

    ax.set_ylabel("Context Switches")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Annotate bars with values
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        fontsize=9)

    add_labels(rects1)
    add_labels(rects2)

    fig.savefig(os.path.join(results_dir, filename))
    plt.close(fig)

# Create and save the context switch comparison plot
save_context_switch_comparison_plot(
    isrr_context_switches,
    srr_context_switches,
    ["Case I", "Case II", "Case III"],
    "Context Switch Comparison",
    "Context_Switch_Comparison.png",
    results_dir
)


print("Graphs have been saved to:", os.path.abspath(results_dir))

