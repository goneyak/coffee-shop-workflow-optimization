import os
import csv
import numpy as np

from src.simulation import simulate
from src.config import SIM_TIME_HOURS, DT, RUNS, ARRIVAL_RATE, SCENARIOS


def run_scenario(name, mu0, mu1, mu2, runs=RUNS, base_seed=1000):
    avg_queues = []
    throughputs = []

    for i in range(runs):
        out = simulate(
            arrival_rate=ARRIVAL_RATE,
            mu0=mu0,
            mu1=mu1,
            mu2=mu2,
            sim_time_hours=SIM_TIME_HOURS,
            dt=DT,
            seed=base_seed + i
        )
        avg_queues.append(out["avg_queue_length"])
        throughputs.append(out["throughput"])

    avg_queues = np.array(avg_queues)
    throughputs = np.array(throughputs)

    mean_queue = float(np.mean(avg_queues))
    std_queue = float(np.std(avg_queues, ddof=1))

    mean_throughput = float(np.mean(throughputs))
    std_throughput = float(np.std(throughputs, ddof=1))

    # Little's Law proxy
    mean_wait_approx = float(mean_queue / mean_throughput) if mean_throughput > 0 else float("nan")

    return {
        "scenario": name,
        "mu0": mu0,
        "mu1": mu1,
        "mu2": mu2,
        "mean_avg_queue": mean_queue,
        "std_avg_queue": std_queue,
        "mean_throughput": mean_throughput,
        "std_throughput": std_throughput,
        "mean_wait_approx": mean_wait_approx,
        "runs": runs
    }


def run_all_scenarios():
    rows = []

    for name, params in SCENARIOS.items():
        mu0 = params["mu0"]
        mu1 = params["mu1"]
        mu2 = params["mu2"]

        row = run_scenario(name, mu0, mu1, mu2)
        rows.append(row)

    return rows


def save_csv(rows, out_path="results/summary.csv"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    fieldnames = [
        "scenario", "mu0", "mu1", "mu2",
        "mean_avg_queue", "std_avg_queue",
        "mean_throughput", "std_throughput",
        "mean_wait_approx",
        "runs"
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


if __name__ == "__main__":
    rows = run_all_scenarios()
    save_csv(rows)
    print("Saved results to results/summary.csv")
    for r in rows:
        print(r)