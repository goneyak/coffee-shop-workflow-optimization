# Coffee Shop Workflow Optimization  
### A Stochastic Queue Simulation for Bottleneck Analysis

---

## Why This Project Exists

High-volume service systems often suffer from congestion, but frontline feedback frequently attributes delays to individual performance rather than structural design.

This project reframes the problem:

> Is delay caused by people — or by system architecture?

Using queueing theory and stochastic simulation, this model quantifies how workflow structure — not individual mistakes — drives congestion in a real-world coffee shop environment.

---

## System Modeled

```
Arrival → Till → Shots → Milk → Exit
```

Three sequential service stages:

- **Till (μ0):** Order entry, payment handling, loyalty enrollment, upselling  
- **Shots (μ1):** Espresso extraction  
- **Milk (μ2):** Milk steaming and specialty preparation  

Customers must pass through all stages.

---

## Modeling Approach

### Arrival Process

```
A_t ~ Poisson(λ * dt)
```

Customers arrive randomly with average rate λ (customers/hour).

---

### Service Process

```
S_{i,t} ~ Poisson(μ_i * dt)
```

Each station has stochastic service capacity:

- μ0 = Till rate  
- μ1 = Shots rate  
- μ2 = Milk rate  

---

## Performance Metrics

We evaluate:

- **Average queue length (L̄)**
- **Throughput**
- **Time-in-system proxy (W ≈ L̄ / Throughput)**

Little’s Law:

```
L = λW
```

---

# Results & Interpretation

### Baseline (Observed Workflow)

| Metric | Value |
|--------|-------|
| Avg Queue Length | 14.05 |
| Throughput | 57.9 orders/hour |
| Estimated Time in System | ~14.6 minutes |

System remains stable (λ < μ0), but queues build during high-utilization periods.

---

### Scenario 1: Improved Till Efficiency

(μ0 increased via streamlined POS flow / reduced friction)

| Metric | Value |
|--------|-------|
| Avg Queue Length | 9.61 |
| Throughput | 59.0 orders/hour |
| Estimated Time in System | ~9.8 minutes |

**Impact:**  
~30–35% reduction in congestion with modest Till improvement.

---

### Scenario 2: Full Improvement (Till + Bar)

| Metric | Value |
|--------|-------|
| Avg Queue Length | 7.24 |
| Throughput | 59.0 orders/hour |
| Estimated Time in System | ~7.4 minutes |

Marginal gains from bar improvement once Till is stabilized.

---

## Key Insight

The model reveals:

- The Till stage is the structural bottleneck.
- Small improvements in Till service rate produce disproportionately large reductions in congestion.
- Downstream optimization (Shots, Milk) yields limited returns if the upstream constraint remains.

This reflects classical high-utilization queue behavior:

```
ρ = λ / μ
```

As utilization (ρ) approaches 1, queue growth becomes nonlinear.

---

## Strategic Implication

Operational delay in high-volume environments is often misattributed to individual performance.

This simulation demonstrates:

- Congestion is a **system-level phenomenon**
- Bottlenecks shift leverage points
- Micro-efficiency improvements upstream dominate downstream tuning

---

## Broader Relevance

Although modeled on a coffee shop, this structure generalizes to:

- Hospital triage → Diagnostics → Treatment  
- Insurance intake → Review → Approval  
- EHR entry → Clinical processing → Discharge  

Serial high-utilization systems behave similarly across domains.

---

## What This Project Demonstrates

- Applied queueing theory in a real operational setting  
- Translation of qualitative observation into quantitative modeling  
- Structural bottleneck identification  
- Data-driven operational reasoning  

---

## Future Extensions

Planned improvements:

- Time-varying arrival rates (peak modeling)  
- Menu-dependent service times  
- Learning curve effects  
- Multi-server Till configuration  
- Healthcare operations analog modeling  

---
