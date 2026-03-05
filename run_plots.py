#!/usr/bin/env python3
import sys
import os
import traceback

os.chdir("/Users/cocoxoxo/coffee-shop-workflow-optimization")
sys.path.insert(0, "/Users/cocoxoxo/coffee-shop-workflow-optimization")

try:
    from src.plotting import (
        plot_multi_server_line,
        plot_peak_arrivals_queue,
        plot_menu_mix_pies,
        plot_server_queue_heatmap,
        plot_scenario_comparison,
        plot_utilization_curve,
    )

    print("Running plot_multi_server_line...")
    plot_multi_server_line()

    print("Running plot_peak_arrivals_queue...")
    plot_peak_arrivals_queue()

    print("Running plot_menu_mix_pies...")
    plot_menu_mix_pies()

    print("Running plot_server_queue_heatmap...")
    plot_server_queue_heatmap()

    print("Running plot_scenario_comparison...")
    plot_scenario_comparison()

    print("Running plot_utilization_curve...")
    plot_utilization_curve()

    print("\nDone! Files in results/:")
    for f in sorted(os.listdir("results")):
        if f.endswith(".png"):
            print(f"  {f}")
except Exception as e:
    traceback.print_exc()
    sys.exit(1)
