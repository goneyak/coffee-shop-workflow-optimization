import os
import csv
import matplotlib.pyplot as plt


def load_summary(csv_path="results/summary.csv"):
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # numeric columns convert
            r["mean_avg_queue"] = float(r["mean_avg_queue"])
            r["std_avg_queue"] = float(r["std_avg_queue"])
            r["mean_throughput"] = float(r["mean_throughput"])
            r["std_throughput"] = float(r["std_throughput"])
            r["mean_wait_approx"] = float(r["mean_wait_approx"])
            rows.append(r)
    return rows


def bar_plot(x_labels, values, title, ylabel, out_path):
    plt.figure()
    plt.bar(x_labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def main():
    os.makedirs("results", exist_ok=True)

    rows = load_summary("results/summary.csv")
    scenarios = [r["scenario"] for r in rows]

    avg_queues = [r["mean_avg_queue"] for r in rows]
    throughputs = [r["mean_throughput"] for r in rows]
    waits = [r["mean_wait_approx"] for r in rows]

    bar_plot(
        scenarios,
        avg_queues,
        title="Average Queue Length by Scenario (Monte Carlo mean)",
        ylabel="Avg queue length (customers)",
        out_path="results/avg_queue_by_scenario.png"
    )

    bar_plot(
        scenarios,
        throughputs,
        title="Throughput per Hour by Scenario (Monte Carlo mean)",
        ylabel="Throughput (customers/hour)",
        out_path="results/throughput_by_scenario.png"
    )

    bar_plot(
        scenarios,
        waits,
        title="Approx. Time-in-System by Scenario (Little's Law proxy)",
        ylabel="Hours",
        out_path="results/wait_proxy_by_scenario.png"
    )

    print("Saved plots to results/:")
    print("- results/avg_queue_by_scenario.png")
    print("- results/throughput_by_scenario.png")
    print("- results/wait_proxy_by_scenario.png")


if __name__ == "__main__":
    main()