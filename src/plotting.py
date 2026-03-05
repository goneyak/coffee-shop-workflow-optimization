import os
import csv
import glob
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.simulation import simulate


# ── 1. 서버 수별 처리량/대기열 라인그래프 ──────────────────────────────────────
def plot_multi_server_line():
    files = sorted(glob.glob("results/multi_server_*/summary.csv"))
    server_counts, avg_queues, throughputs, std_queues = [], [], [], []
    for f in files:
        df = pd.read_csv(f)
        server_counts.append(int(df["servers_till"].iloc[0]))
        avg_queues.append(df["mean_avg_queue"].iloc[0])
        std_queues.append(df["std_avg_queue"].iloc[0])
        throughputs.append(df["mean_throughput"].iloc[0])

    fig, ax1 = plt.subplots(figsize=(7, 4))
    color1, color2 = "#2196F3", "#FF5722"
    ax2 = ax1.twinx()

    ax1.errorbar(server_counts, avg_queues, yerr=std_queues,
                 color=color1, marker="o", linewidth=2, capsize=4, label="Avg Queue Length")
    ax2.plot(server_counts, throughputs, color=color2, marker="s",
             linewidth=2, linestyle="--", label="Throughput (orders/hr)")

    ax1.set_xlabel("Number of Till Servers")
    ax1.set_ylabel("Avg Queue Length", color=color1)
    ax2.set_ylabel("Throughput (orders/hr)", color=color2)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax2.tick_params(axis="y", labelcolor=color2)
    ax1.set_xticks(server_counts)
    ax1.set_xticklabels([f"{s} server(s)" for s in server_counts])

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")
    plt.title("Queue & Throughput by Till Server Count")
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/multi_server_lineplot.png", dpi=200)
    plt.close()
    print("✓ results/multi_server_lineplot.png")


# ── 2. peak_arrivals 시간대별 queue 변화 ──────────────────────────────────────
def plot_peak_arrivals_queue():
    with open("configs/peak_arrivals.yaml") as f:
        config = yaml.safe_load(f)

    peak_profile = config.get("arrival", {}).get("peak_profile", None)
    result = simulate(
        arrival_rate=60,
        mu0=65, mu1=85, mu2=75,
        sim_time_hours=8,
        dt=0.005,
        seed=42,
        peak_profile=peak_profile,
        preorder_enabled=False,
        servers=(1, 1, 1),
        menu_config=None,
    )
    q_series = result["queue_series"]
    t = np.linspace(0, 8, len(q_series))

    # peak_profile 범위 색칠
    peak_colors = ["#bbdefb", "#64b5f6", "#1565c0", "#42a5f5"]
    fig, ax = plt.subplots(figsize=(9, 4))
    if peak_profile:
        for i, (s, e, rate) in enumerate(peak_profile):
            ax.axvspan(s, e, alpha=0.15, color=peak_colors[i % len(peak_colors)],
                       label=f"{s}–{e}h  λ={rate}/hr")

    ax.plot(t, q_series, color="#d32f2f", linewidth=1.2, label="Total Queue")
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Queue Length (customers)")
    ax.set_title("Queue Length Over Time — Peak Arrivals Scenario")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/peak_arrivals_queue_plot.png", dpi=200)
    plt.close()
    print("✓ results/peak_arrivals_queue_plot.png")


# ── 3. menu_mix 파이차트 ────────────────────────────────────────────────────
def plot_menu_mix_pies():
    configs = {
        "Normal Mix":      "configs/menu_normal_mix.yaml",
        "Milk Heavy":      "configs/menu_milk_heavy.yaml",
        "Quick Drinks":    "configs/menu_quick_drinks.yaml",
    }
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    for ax, (title, path) in zip(axes, configs.items()):
        with open(path) as f:
            cfg = yaml.safe_load(f)
        raw_mix = cfg.get("menu_mix", {})
        # filter out non-numeric entries (e.g. nested service_times_hours key in yaml)
        mix = {k: float(v) for k, v in raw_mix.items()
               if isinstance(v, (int, float))}
        labels = list(mix.keys())
        sizes  = list(mix.values())
        wedges, texts, autotexts = ax.pie(
            sizes, labels=None, autopct="%1.1f%%", startangle=90,
            pctdistance=0.80,
            wedgeprops=dict(linewidth=0.5, edgecolor="white"))
        for at in autotexts:
            at.set_fontsize(7)
        ax.legend(wedges, labels, loc="lower center", fontsize=7,
                  ncol=2, bbox_to_anchor=(0.5, -0.25))
        ax.set_title(title, fontsize=11, fontweight="bold")
    plt.suptitle("Menu Mix by Scenario", fontsize=13, fontweight="bold", y=1.01)
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/menu_mix_piechart.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("✓ results/menu_mix_piechart.png")


# ── 4. 시나리오별 서버별 큐 분포 히트맵 ──────────────────────────────────────
def plot_server_queue_heatmap():
    scenario_files = {
        "baseline":            "results/baseline/summary.csv",
        "improved_till":       "results/improved_till/summary.csv",
        "full_improvement":    "results/full_improvement/summary.csv",
        "multi_server_1":      "results/multi_server_1/summary.csv",
        "multi_server_2":      "results/multi_server_2/summary.csv",
        "multi_server_3":      "results/multi_server_3/summary.csv",
        "preorder_buffer":     "results/preorder_buffer_large/summary.csv",
        "peak_arrivals":       "results/peak_arrivals/summary.csv",
    }
    rows = []
    scenario_names = []
    for name, path in scenario_files.items():
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        q0 = float(df["mean_q0"].iloc[0]) if "mean_q0" in df.columns else 0.0
        q1 = float(df["mean_q1"].iloc[0]) if "mean_q1" in df.columns else 0.0
        q2 = float(df["mean_q2"].iloc[0]) if "mean_q2" in df.columns else 0.0
        rows.append([q0, q1, q2])
        scenario_names.append(name)

    matrix = np.array(rows)
    stage_labels = ["Till (q0)", "Shots (q1)", "Milk (q2)"]

    fig, ax = plt.subplots(figsize=(6, max(4, len(scenario_names) * 0.55 + 1)))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(3))
    ax.set_xticklabels(stage_labels, fontsize=10)
    ax.set_yticks(range(len(scenario_names)))
    ax.set_yticklabels(scenario_names, fontsize=9)
    plt.colorbar(im, ax=ax, label="Mean Queue Length")
    for i in range(len(scenario_names)):
        for j in range(3):
            val = matrix[i, j]
            ax.text(j, i, f"{val:.1f}",
                    ha="center", va="center", fontsize=8,
                    color="black" if val < matrix.max() * 0.6 else "white")
    ax.set_title("Per-Stage Queue Length by Scenario", fontsize=12, fontweight="bold")
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/server_queue_heatmap.png", dpi=200)
    plt.close()
    print("✓ results/server_queue_heatmap.png")


# ── 5. 종합 시나리오 비교 bar chart (throughput + avg_queue) ──────────────────
def plot_scenario_comparison():
    scenario_files = {
        "baseline":          "results/baseline/summary.csv",
        "improved_till":     "results/improved_till/summary.csv",
        "full_improvement":  "results/full_improvement/summary.csv",
        "multi_server_1":    "results/multi_server_1/summary.csv",
        "multi_server_2":    "results/multi_server_2/summary.csv",
        "multi_server_3":    "results/multi_server_3/summary.csv",
        "preorder_buffer":   "results/preorder_buffer_large/summary.csv",
        "peak_arrivals":     "results/peak_arrivals/summary.csv",
        "visible_queue":     "results/visible_queue/summary.csv",
    }
    names, queues, stds, throughputs = [], [], [], []
    for name, path in scenario_files.items():
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        names.append(name)
        queues.append(df["mean_avg_queue"].iloc[0])
        stds.append(df["std_avg_queue"].iloc[0])
        throughputs.append(df["mean_throughput"].iloc[0])

    x = np.arange(len(names))
    width = 0.4
    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax2 = ax1.twinx()
    bars = ax1.bar(x - width / 2, queues, width, yerr=stds, capsize=3,
                   color="#5c85d6", alpha=0.85, label="Avg Queue Length")
    ax2.bar(x + width / 2, throughputs, width,
            color="#f4a442", alpha=0.85, label="Throughput (orders/hr)")
    ax1.set_ylabel("Avg Queue Length", color="#5c85d6")
    ax2.set_ylabel("Throughput (orders/hr)", color="#f4a442")
    ax1.tick_params(axis="y", labelcolor="#5c85d6")
    ax2.tick_params(axis="y", labelcolor="#f4a442")
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=25, ha="right", fontsize=8)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)
    ax1.set_title("Scenario Comparison: Queue Length & Throughput", fontsize=12, fontweight="bold")
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/scenario_comparison.png", dpi=200)
    plt.close()
    print("✓ results/scenario_comparison.png")


# ── 6. 활용률(ρ) vs 평균 queue 길이 곡선 ────────────────────────────────────
def plot_utilization_curve():
    df = pd.read_csv("results/utilization_summary.csv")
    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax2 = ax1.twinx()
    ax1.plot(df["rho_pct"], df["mean_queue"], color="#e53935", marker="o",
             linewidth=2, label="Avg Queue Length")
    ax2.plot(df["rho_pct"], df["throughput"], color="#43a047", marker="s",
             linewidth=2, linestyle="--", label="Throughput (orders/hr)")
    ax1.set_xlabel("Server Utilization ρ (%)")
    ax1.set_ylabel("Avg Queue Length", color="#e53935")
    ax2.set_ylabel("Throughput (orders/hr)", color="#43a047")
    ax1.tick_params(axis="y", labelcolor="#e53935")
    ax2.tick_params(axis="y", labelcolor="#43a047")
    ax1.axvline(x=80, color="gray", linestyle=":", alpha=0.7, label="ρ=80% threshold")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)
    ax1.set_title("Utilization vs Queue & Throughput", fontsize=12, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/utilization_curve.png", dpi=200)
    plt.close()
    print("✓ results/utilization_curve.png")


def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print("=== Generating all visualizations ===")
    plot_multi_server_line()
    plot_peak_arrivals_queue()
    plot_menu_mix_pies()
    plot_server_queue_heatmap()
    plot_scenario_comparison()
    plot_utilization_curve()
    print("\nAll plots saved to results/")


if __name__ == "__main__":
    main()
