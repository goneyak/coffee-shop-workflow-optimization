import os
import csv
import numpy as np
import yaml

from src.simulation import simulate


def run_scenario(name, mu0, mu1, mu2, runs=300, base_seed=1000, arrival_rate=60, sim_time_hours=8, dt=0.005, peak_profile=None, preorder_enabled=False, servers=(1,1,1), menu_config=None):
    avg_queues = []
    throughputs = []
    avg_q0s = []
    avg_q1s = []
    avg_q2s = []
    peak_q0s = []
    peak_totals = []

    for i in range(runs):
        out = simulate(
            arrival_rate=arrival_rate,
            mu0=mu0,
            mu1=mu1,
            mu2=mu2,
            sim_time_hours=sim_time_hours,
            dt=dt,
            seed=base_seed + i,
            peak_profile=peak_profile,
            preorder_enabled=preorder_enabled,
            servers=servers,
            menu_config=menu_config
        )
        avg_queues.append(out["avg_queue_length"])
        throughputs.append(out["throughput"])
        
        # Collect additional metrics for visible queue analysis
        avg_q0s.append(out["avg_q0"])
        avg_q1s.append(out["avg_q1"])
        avg_q2s.append(out["avg_q2"])
        peak_q0s.append(out["peak_q0"])
        peak_totals.append(out["peak_total"])

    avg_queues = np.array(avg_queues)
    throughputs = np.array(throughputs)
    avg_q0s = np.array(avg_q0s)
    avg_q1s = np.array(avg_q1s)
    avg_q2s = np.array(avg_q2s)
    peak_q0s = np.array(peak_q0s)
    peak_totals = np.array(peak_totals)

    mean_queue = float(np.mean(avg_queues))
    std_queue = float(np.std(avg_queues, ddof=1))

    mean_throughput = float(np.mean(throughputs))
    std_throughput = float(np.std(throughputs, ddof=1))

    # Little's Law proxy
    mean_wait_approx = float(mean_queue / mean_throughput) if mean_throughput > 0 else float("nan")
    
    # Additional metrics
    mean_q0 = float(np.mean(avg_q0s))
    mean_q1 = float(np.mean(avg_q1s))
    mean_q2 = float(np.mean(avg_q2s))
    mean_peak_q0 = float(np.mean(peak_q0s))
    mean_peak_total = float(np.mean(peak_totals))

    s0, s1, s2 = servers
    return {
        "scenario": name,
        "mu0": mu0,
        "mu1": mu1,
        "mu2": mu2,
        "servers_till": s0,
        "servers_shots": s1,
        "servers_milk": s2,
        "mean_avg_queue": mean_queue,
        "std_avg_queue": std_queue,
        "mean_throughput": mean_throughput,
        "std_throughput": std_throughput,
        "mean_wait_approx": mean_wait_approx,
        "mean_q0": mean_q0,
        "mean_q1": mean_q1,
        "mean_q2": mean_q2,
        "mean_peak_q0": mean_peak_q0,
        "mean_peak_total": mean_peak_total,
        "runs": runs
    }


def save_csv(rows, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    fieldnames = [
        "scenario", "mu0", "mu1", "mu2",
        "servers_till", "servers_shots", "servers_milk",
        "mean_avg_queue", "std_avg_queue",
        "mean_throughput", "std_throughput",
        "mean_wait_approx",
        "mean_q0", "mean_q1", "mean_q2",
        "mean_peak_q0", "mean_peak_total",
        "runs"
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run coffee shop simulation experiments")
    parser.add_argument('--config', default='configs/baseline.yaml', help='Path to config YAML file')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    experiment_name = config['experiment_name']
    sim_time_hours = config['sim_time_hours']
    dt = config['dt']
    runs = config['runs']
    arrival_rate = config['arrival']['lambda_per_hour'] if config['arrival']['type'] == 'constant' else config['arrival'].get('lambda_per_hour', 60)
    
    # Handle menu config first (if present)
    menu_config = None
    if 'menu_mix' in config and 'modifiers' in config and 'service_times_seconds' in config:
        menu_config = {
            'menu_mix': config['menu_mix'],
            'modifiers': config['modifiers'],
            'service_times_hours': config['service_times_hours']
        }
        # For menu-based experiments, mu values are ignored (dummy values)
        mu0, mu1, mu2 = 65, 85, 75
    else:
        # Classic config with explicit service rates
        mu0 = config['service']['till']['mu_per_hour']
        mu1 = config['service']['shots']['mu_per_hour']
        mu2 = config['service']['milk']['mu_per_hour']
    
    # servers
    if 'staffing' in config:
        # Menu config uses 'staffing' key
        s0 = config['staffing'].get('till_servers', 1)
        s1 = config['staffing'].get('shots_servers', 1)
        s2 = config['staffing'].get('milk_servers', 1)
    else:
        # Classic config uses 'service' key
        s0 = config['service']['till'].get('servers', 1)
        s1 = config['service']['shots'].get('servers', 1)
        s2 = config['service']['milk'].get('servers', 1)
    
    # Handle peak profile if time_varying
    peak_profile = None
    if config['arrival']['type'] == 'time_varying' and 'peak_profile' in config['arrival']:
        peak_profile = config['arrival']['peak_profile']
    
    # Handle policy
    preorder_enabled = False
    if 'policy' in config and 'preorder_buffer' in config['policy']:
        preorder_enabled = config['policy']['preorder_buffer']['enabled']

    row = run_scenario(
        experiment_name, mu0, mu1, mu2,
        runs=runs,
        arrival_rate=arrival_rate,
        sim_time_hours=sim_time_hours,
        dt=dt,
        peak_profile=peak_profile,
        preorder_enabled=preorder_enabled,
        servers=(s0, s1, s2),
        menu_config=menu_config
    )
    rows = [row]

    out_path = f"results/{experiment_name}/summary.csv"
    save_csv(rows, out_path)
    print(f"Saved results to {out_path}")
    print(row)