# Coffee Shop Workflow Optimization
### A Stochastic Queue Simulation for Bottleneck Analysis

---

# Overview

High-volume service systems often experience congestion, yet delays are frequently attributed to individual performance rather than structural workflow design.

This project explores a different question:

> Are delays caused by people — or by system architecture?

Using queueing theory and stochastic simulation, this repository models the operational workflow of a high-volume coffee shop and analyzes how structural bottlenecks emerge in sequential service systems.

Although the model is inspired by a coffee shop environment, the system structure generalizes to many service operations such as:

- hospital triage → diagnostics → treatment
- insurance intake → review → approval
- customer support ticket processing

---

# System Workflow Modeled

The workflow is modeled as a **three-stage serial service system**:

```
Arrival → Till → Shots → Milk → Exit
```

Where:

| Stage | Description |
|-----|-----|
| Till (μ₀) | Order entry, payment processing, loyalty enrollment, upselling |
| Shots (μ₁) | Espresso extraction |
| Milk (μ₂) | Milk steaming and specialty drink preparation |

Each customer must pass sequentially through all stages.

**Model Simplification:** This three-stage serial model abstracts the actual workflow to isolate structural bottlenecks. Real operations include parallel preparation, customer wait zones, and floor operations. However, the sequential queueing structure accurately captures the primary congestion dynamics at high utilization. The model is intentionally simplified to demonstrate how small inefficiencies in constrained stages produce system-wide delays.

---

# Modeling Approach

This project implements a **discrete-time stochastic simulation** of a multi-stage queueing system.

## Arrival Process

Customer arrivals follow a Poisson process:

```
A_t ~ Poisson(λ * dt)
```

Where:

- λ = average arrival rate (customers/hour)
- dt = simulation time step

This models random customer arrivals with no memory.

---

## Service Process

Each station has stochastic service capacity per time step:

```
S_{i,t} ~ Poisson(μ_i * dt)
```

Where:

- μ₀ = Till service rate
- μ₁ = Shots service rate
- μ₂ = Milk service rate

At each step:

```
served = min(queue, service_capacity)
```

Customers are then passed to the next stage.

---

# Performance Metrics

The simulation evaluates three main metrics.

## 1. Average System Size

```
L̄ = (1/T) Σ L_t
```

Where

```
L_t = q0 + q1 + q2
```

This represents the **average number of customers in the system**.

Important:

- This includes customers waiting **and being served**
- It does **not only represent the visible queue**
- In this project, `q0`, `q1`, `q2` are treated as **work-in-progress (WIP) counts** at each stage (waiting + in-service).

---

## 2. Throughput

```
Throughput = completed_orders / simulation_time
```

This measures how many orders the system can process per hour.

---

## 3. Estimated Time in System

Using Little's Law:

```
L = λW
```

We estimate:

```
W ≈ L̄ / Throughput
```

This approximates the **average time a customer spends inside the system**, using throughput as the empirical effective arrival rate in steady operation.

---

# Baseline Simulation Results

Baseline parameters represent the observed workflow structure.

**Note:** L̄ represents **total system work-in-progress** (q0 + q1 + q2). Visible queue (q0 only) is analyzed separately in Scenario 4.

| Metric | Baseline | Improved Till | Full Improvement | Peak Arrivals | Preorder Small | Preorder Large |
|--------|----------|---------------|------------------|---------------|----------------|----------------|
| **Avg Queue Length (L̄)** | 14.05 | 9.61 | 7.24 | 51.15 | 12.02 | 12.02 |
| **Throughput (orders/hr)** | 57.90 | 59.03 | 59.01 | 54.02 | 57.90 | 57.90 |
| **Wait Time Approx (hours)** | 0.243 | 0.163 | 0.123 | 0.947 | 0.208 | 0.208 |
| **Wait Time (minutes)** | ~14.6 | ~9.8 | ~7.4 | ~57 | ~12.5 | ~12.5 |

**Key Observations:**

- **Observed Throughput Ceiling (baseline settings):** Throughput stays in a narrow band (about 54-59 orders/hour in these experiments), consistent with a bottleneck-limited serial system under heavy load.
- **Improved Till** (~32% congestion reduction): Till efficiency alone yields significant gains, reducing queue from 14 to 9.6 orders.
- **Full Improvement** (~48% congestion reduction): Additional bar-stage improvements have diminishing returns, showing the bottleneck-relief principle.
- **Peak Arrivals** (lunch-hour rush 5-7pm): Demonstrates system fragility under demand spikes; queue grows 3.6× while throughput drops only 7%.
- **Preorder Buffering** (~14% congestion reduction): Priority handling at the Shots stage can reduce internal queue accumulation while maintaining similar throughput in current settings.
- **Additional Till servers** (Scenario 6): Adding a second till more than halves system congestion and wait time; a third till yields only marginal extra gain due to downstream bottlenecks. Staffing is therefore a powerful lever for managing utilization.

---

# Scenario Analysis

The simulation evaluates potential operational improvements.

---

## Scenario 1 — Improved Till Efficiency

This scenario increases μ₀ by modeling a streamlined ordering process.

Possible real-world mechanisms include:

- faster POS interaction
- reduced friction in loyalty enrollment
- simplified upselling workflow

**Result:** ~30–35% reduction in congestion.

---

## Scenario 2 — Full Workflow Improvement

This scenario increases service rates at all stages.

**Result:** Additional improvements occur, but with diminishing returns once the upstream bottleneck is relieved.

---

## Scenario 3 — Peak Arrivals (Time-Varying Demand)

This scenario explores system behavior under lunch-hour rush conditions (0-3hr: 40/hr, 3-5hr: 80/hr, 5-7hr: 120/hr, 7-8hr: 70/hr).

**Note on realism:** At 120/hr arrival rate, real systems experience customer abandonment (balking/reneging). This scenario shows theoretical system limits without behavioral constraints—a common approach in operations research to quantify structural bottleneck severity.

**Result:** Queue length grows 3.6× to 51 customers while throughput drops only 7% (57.9→54.0), demonstrating that demand spikes primarily create waiting rather than increased service capacity.

---

## Scenario 4 — Visible Queue vs System Backlog

This scenario analyzes the **customer perception gap** during peak hours.

**Stress-test setup used for this scenario:**

| Parameter | Value |
|-----------|-------|
| Arrival profile | 0-3h: 40/hr, 3-5h: 80/hr, 5-7h: 120/hr, 7-8h: 70/hr |
| Service rates | mu0=65, mu1=85, mu2=75 (orders/hr equivalent in base mode) |
| Simulation horizon | 8 hours |
| Time step | dt=0.005 hours |

We use a smaller `dt` in stress tests to reduce discretization artifacts under high arrival variability.

**Key Insight:** Customers only see the Till line, but significant work accumulates behind the counter.

| Queue Component | Average Length | Peak Length | % of Total |
|----------------|----------------|-------------|-----------|
| **Visible Queue (Till)** | 45.5 | 155 | 89% |
| **Bar Backlog (Shots)** | 2.1 | - | 4% |
| **Bar Backlog (Milk)** | 3.6 | - | 7% |
| **Total System** | 51.1 | 165 | 100% |

**Reality Check:** During lunch rush, customers see ~45 people in line, but the system actually has 51 orders in progress. The remaining 6 orders are "invisible" work-in-progress behind the bar.

**Operational Insight:** This customer perception gap is endemic to service systems:
- Hospital triage: Patient sees waiting room, but diagnosis/treatment backlog is hidden
- Airport security: Visible queue is short, but TSA agents process bottleneck behind scenes  
- Call centers: Customer wait time reflects overall system load, not just visible queue

**Implication:** Reducing visible queue alone (e.g., through preorder buffers) doesn't reduce operational stress; it redistributes congestion upstream. True improvement requires addressing the throughput ceiling.

---

## Scenario 5 — Pipeline Preparation Policy

*(See [docs/05_preorder_buffer.md](docs/05_preorder_buffer.md) for full notes.)*

This scenario models a preorder-style buffering rule where orders that leave Till are placed in a priority buffer for Shots before regular queue items.

**Policy mechanism (as implemented):** Till-completed orders are routed to a priority queue (`preorder_q1`) and consumed first by the Shots stage within available service budget.

**Trade-off Analysis:**
- **System congestion reduction:** L̄ decreases from 14.05 to 12.02 (-14%)
- **Visible queue (q0):** Essentially unchanged (Till throughput unaffected)
- **Shots queue (q1):** Becomes near-zero on average (priority buffer absorbs most intermediate buildup)
- **Throughput:** Maintained at 57.90 orders/hr (no change—Milk capacity still constrains system)

**Operational Lesson:** In this model, preorder buffering mainly redistributes queueing across stages rather than increasing system capacity. It can smooth intermediate buildup at Shots while overall throughput remains constrained by downstream limits.

---

## Scenario 6 — Multi-Server Till

This experiment varies the number of parallel servers at the Till while keeping
all other parameters constant (μ₀=65, μ₁=85, μ₂=75). It simulates `c0 = 1, 2,
3` tills to quantify how staffing affects congestion and wait.

| Till servers | Avg Queue (L̄) | Throughput | Wait (min) |
|--------------|----------------|------------|------------|
| 1 (baseline) | 14.05          | 57.90      | ~14.6      |
| 2            | 6.64           | 59.32      | ~6.7       |
| 3            | 6.14           | 59.40      | ~6.2       |

**Interpretation:** Adding a second till dramatically reduces the average
number of customers in the system and cuts wait times by more than half. A
third till yields diminishing returns because the downstream bar stages become
the binding bottleneck. Throughput remains roughly constant, once again
highlighting that capacity is limited by the slowest stage (here μ₂ at Milk).

**Operational Lesson:** Staffing (c₀) is a powerful lever for controlling
expected queue lengths without changing the underlying service rates. The
results here mirror classic M/M/c queueing behavior: as utilization per server
decreases, both variability and queueing delay drop sharply.

---

# Key Insight

## Bottleneck Principle

In serial queueing systems, congestion is dominated by the **slowest or most constrained upstream stage**.

Utilization is defined as:

```
ρ = λ / μ
```

When utilization approaches 1:

- variability increases
- queues grow nonlinearly
- small service improvements produce large congestion reductions

In this model, the **Till stage appears as the primary bottleneck in baseline settings**, and bottlenecks can shift downstream after interventions.

---

## Utilization Curve (The Fundamental Law)

One of the most important discoveries in operations research is that **queue length grows nonlinearly with utilization** and tends to blow up as rho approaches 1.

### Results from sweep (ρ = 0.2 to 0.95)

| ρ (Utilization) | L̄ (avg queue) | Wait time |
|-----------------|----------------|-----------|
| 0.20            | 0.55           | ~2.5 min  |
| 0.40            | 1.46           | ~3.4 min  |
| 0.60            | 3.10           | ~4.8 min  |
| 0.80            | 7.12           | ~8.3 min  |
| 0.90            | 12.15          | ~12.9 min |
| 0.95            | 16.69          | ~17.1 min |

### The "Knee" at ρ ≈ 0.75–0.85

Below ρ = 0.7, system behavior is **predictable and stable**.  
Above ρ = 0.85, the system enters a **danger zone** where small demand increases cause explosive queue growth.

### Operational Implication

A coffee shop designed for average demand may be comfortable at ρ = 0.6. But when demand spikes (peak hours) pushing toward ρ = 0.9, wait times don't double — they **triple or quadruple**. This is why **spare capacity matters**.

For detailed analysis, see [docs/07_utilization_analysis.md](docs/07_utilization_analysis.md).

---

# Repository Structure

```
coffee-shop-workflow-optimization/
├── src/
│   ├── simulation.py         # Core discrete-time stochastic simulator
│   ├── experiments.py        # Monte Carlo experiment runner
│   ├── config.py             # Baseline scenario parameters
│   └── plotting.py           # All visualizations (6 chart types)
├── configs/
│   ├── baseline.yaml         # Baseline scenario
│   ├── improved_till.yaml    # Scenario 1: improved till efficiency
│   ├── full_improvement.yaml # Scenario 2: full workflow improvement
│   ├── peak_arrivals.yaml    # Scenario 3: time-varying peak demand
│   ├── visible_queue.yaml    # Scenario 4: visible queue vs backlog
│   ├── preorder_buffer_*.yaml  # Scenario 5: preorder pipeline
│   ├── multi_server_*.yaml   # Scenario 6: multi-server till (1–3 servers)
│   ├── menu_*.yaml           # Scenario 7: menu-dependent service times
│   └── utilization_*.yaml    # Utilization sweep (ρ = 0.2 → 0.95)
├── results/
│   ├── <scenario>/summary.csv     # Per-scenario Monte Carlo results
│   ├── utilization_summary.csv    # Utilization sweep aggregated
│   ├── scenario_comparison.png    # Throughput & queue across all scenarios
│   ├── multi_server_lineplot.png  # Server count vs queue/throughput
│   ├── peak_arrivals_queue_plot.png # Time-series queue under peak demand
│   ├── menu_mix_piechart.png      # Menu composition by scenario
│   ├── server_queue_heatmap.png   # Per-stage queue heatmap
│   └── utilization_curve.png      # ρ vs queue & throughput curve
├── docs/
│   ├── 00_project_map.md ... 09_healthcare_mapping.md
├── run_plots.py              # Convenience script: regenerate all plots
├── requirements.txt
└── README.md
```

---

# How to Run

### Setup

```bash
git clone https://github.com/goneyak/coffee-shop-workflow-optimization.git
cd coffee-shop-workflow-optimization
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Experiments

```bash
python -m src.experiments
```

Results are saved per-scenario under `results/<scenario>/summary.csv`.

### Regenerate All Plots

```bash
python run_plots.py
```

Generates 6 visualizations in `results/`:

| Plot | Description |
|------|-------------|
| `scenario_comparison.png` | Throughput & queue across all scenarios |
| `multi_server_lineplot.png` | Queue & throughput by till server count |
| `peak_arrivals_queue_plot.png` | Time-series queue under peak demand |
| `menu_mix_piechart.png` | Menu composition (Normal / Milk Heavy / Quick) |
| `server_queue_heatmap.png` | Per-stage queue heatmap across scenarios |
| `utilization_curve.png` | ρ vs queue length & throughput |

---

# Model Scope & Limitations

**Implemented and validated in this project:**
- Time-varying (non-homogeneous Poisson) arrival process
- Multi-server Till (c₀ = 1, 2, 3)
- Preorder buffering (priority queue at Shots stage)
- Utilization sweep (ρ = 0.2 → 0.95)
- Visible queue vs system backlog decomposition
- 300-run Monte Carlo with confidence intervals

**Implemented but still under active validation:**
- Menu-dependent service-time mode (`menu_*.yaml`) and related scenario calibration

**Not modeled (by design):**
- Customer abandonment (balking/reneging)
- Parallel food preparation
- Dynamic staffing or real-time scheduling

These exclusions keep the model focused on structural queueing dynamics.

---

# Why This Project Matters

Many operational delays are attributed to individual performance.

This project demonstrates that congestion is often a **system design problem rather than a people problem**.

By modeling workflow structure explicitly, organizations can identify:

- true structural bottlenecks
- leverage points for improvement
- the disproportionate impact of small operational changes near saturation

The same framework applies directly to healthcare (triage → diagnostics → treatment), insurance processing, and any sequential service system.
