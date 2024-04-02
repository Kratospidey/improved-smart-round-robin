import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

# Dummy results for SRR and ISRR
srr_results = [(37.25, 19.00), (13.20, 8.20), (98.00, 51.50), (15.75, 8.25)]
isrr_results = [(35.00, 16.75), (11.60, 6.60), (84.50, 38.00), (14.50, 7.00)]

# Function to save individual comparison plots with dynamic time quantum
def save_individual_comparison_plot(
    case_number, srr_tat, isrr_tat, srr_wt, isrr_wt, results_dir
):
    labels = ["Average Turnaround time", "Average Waiting Time"]
    srr_values = [srr_tat, srr_wt]
    isrr_values = [isrr_tat, isrr_wt]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, srr_values, width, label=f"SRR", color="#4472c4")
    rects2 = ax.bar(x + width / 2, isrr_values, width, label="ISRR", color="#ed7d31")
    ax.set_ylabel("Time")
    ax.set_title(f"Case {case_number} Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Save the plot to a file
    fig.savefig(os.path.join(results_dir, f"Case_{case_number}_comparison.png"))
    plt.close(fig)

# Function to save cumulative reduction plots with dense striped hatch pattern
def save_reduction_plot(reductions, title, filename, results_dir):
    labels = ["Case I", "Case II", "Case III", "Case IV", "Overall"]
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(x, reductions, width, color="lightblue", hatch="----")

    # Attach a text label above each bar in rects, displaying its height.
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            f"{height:.2f}%",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    # Set the labels, title, and custom x-axis tick labels, etc.
    ax.set_ylabel("Reduction (%)")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(reductions) * 1.15)  # Set y limit to add space for annotations

    fig.tight_layout()

    # Save the figure to the specified directory and file
    fig.savefig(os.path.join(results_dir, filename))
    plt.close(fig)  # Close the plot to avoid displaying in the notebook


# Ensure the results directory exists
results_dir = "../results/SRR_vs_ISRR"
if os.path.isdir(results_dir):
    shutil.rmtree(results_dir)
os.makedirs(results_dir, exist_ok=True)

# Save individual comparison plots for each case
for i, ((srr_tat, srr_wt), (isrr_tat, isrr_wt)) in enumerate(
    zip(srr_results, isrr_results), start=1
):
    save_individual_comparison_plot(
        i, srr_tat, isrr_tat, srr_wt, isrr_wt, results_dir
    )

# Dummy reductions for ATAT and AWT from sRR to iSRR
reductions_atat = [26.96, 15.38, 21.28, 34.615, 24.559]
reductions_awt = [41.98, 18.86, 33.97, 32.65, 31.865]

# Save cumulative reduction plots
save_reduction_plot(
    reductions_atat, "% Reduction in ATAT", "Reduction_ATAT.png", results_dir
)
save_reduction_plot(
    reductions_awt, "% Reduction in AWT", "Reduction_AWT.png", results_dir
)

print("Graphs have been saved to:", os.path.abspath(results_dir))
