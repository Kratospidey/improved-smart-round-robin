import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

# Dummy results for TRR and SRR
trr_results = [(51.0, 32.75), (15.6, 10.6), (124.5, 78.0), (19.5, 12.0)]
srr_results = [(37.25, 19.00), (13.20, 8.20), (98.00, 51.50), (15.75, 8.25)]

# Time quantums for TRR cases, replace these with your actual values
time_quantums = [6, 4, 20, 2]


# Function to save individual comparison plots with dynamic time quantum
def save_individual_comparison_plot(
    case_number, trr_tat, srr_tat, trr_wt, srr_wt, time_quantum, results_dir
):
    labels = ["Average Turnaround time", "Average Waiting Time"]
    trr_values = [trr_tat, trr_wt]
    srr_values = [srr_tat, srr_wt]
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    gap = 0.05  # the gap width between bars in a pair

    fig, ax = plt.subplots()
    rects1 = ax.bar(
        x - (width / 2 + gap / 2),
        trr_values,
        width,
        label=f"TRR (Q={time_quantum})",
        color="#4472c4",
    )
    rects2 = ax.bar(
        x + (width / 2 + gap / 2),
        srr_values,
        width,
        label="SRR",
        color="#ed7d31",
    )

    # Add data labels on top of the bars
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f'{height:.2f}',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom'
            )

    add_labels(rects1)
    add_labels(rects2)

    # Add y-axis grid lines at intervals of 10
    ax.yaxis.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_yticks(np.arange(0, max(trr_values + srr_values) + 10, 10))

    # Set the rest of the labels and title
    ax.set_ylabel('Time')
    ax.set_title(f'Case {case_number} Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Save the plot to a file
    fig.savefig(os.path.join(results_dir, f'Case_{case_number}_comparison.png'))
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
results_dir = "../results/TRR_vs_SRR"
if os.path.isdir(results_dir):
    shutil.rmtree(results_dir)
os.makedirs(results_dir, exist_ok=True)

# Save individual comparison plots for each case
for i, ((trr_tat, trr_wt), (srr_tat, srr_wt), tq) in enumerate(
    zip(trr_results, srr_results, time_quantums), start=1
):
    save_individual_comparison_plot(
        i, trr_tat, srr_tat, trr_wt, srr_wt, tq, results_dir
    )

# Dummy reductions for ATAT and AWT from TRR to SRR
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
