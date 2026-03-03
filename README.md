# Base Model: Multi-Stage Queue Simulation of a High-Volume Coffee Shop

## Overview

This project implements a discrete-time stochastic simulation of a high-volume coffee shop workflow to analyze:

* Queue formation dynamics
* Bottleneck identification
* Operational improvement leverage points

The system is modeled as a multi-stage serial queue reflecting observed real-world operations.

---

## System Architecture

Based on field observations, the workflow is represented as a three-stage serial service system:

```
Arrival → Till → Shots → Milk → Exit
```

Each stage represents a service station:

* **Till (μ₀):** Order entry, payment processing, loyalty program handling, upselling
* **Shots (μ₁):** Espresso extraction
* **Milk (μ₂):** Milk steaming, specialty drink preparation

Customers must pass through each stage sequentially.

---

## Stochastic Assumptions

### 1. Arrival Process

Customer arrivals follow a Poisson process:

[
A_t \sim \text{Poisson}(\lambda \cdot dt)
]

Where:

* λ = average arrival rate (customers per hour)
* dt = simulation time step (e.g., 0.005 hours ≈ 18 seconds)

This assumes arrivals are random and memoryless.

---

### 2. Service Process

Each station has a service capacity drawn from a Poisson distribution:

[
S_{i,t} \sim \text{Poisson}(\mu_i \cdot dt)
]

Where:

* μ₀ = Till service rate
* μ₁ = Shots service rate
* μ₂ = Milk service rate

This models stochastic variation in service speed.

---

## State Variables

At time (t):

* (q_0): Customers waiting at Till
* (q_1): Customers waiting at Shots
* (q_2): Customers waiting at Milk

Total customers in system:

[
L_t = q_0 + q_1 + q_2
]

---

## Simulation Logic (Per Time Step)

1. New arrivals are added to Till queue.
2. Till processes customers and passes them to Shots.
3. Shots processes customers and passes them to Milk.
4. Milk completes orders and customers exit the system.

Each stage processes:

[
\text{served} = \min(\text{queue}, \text{service capacity})
]

---

## Performance Metrics

### 1. Average System Size

[
\bar{L} = \frac{1}{T} \sum_{t=1}^{T} L_t
]

Measures average congestion.

---

### 2. Throughput

[
\text{Throughput} = \frac{\text{completed orders}}{\text{simulation time}}
]

Represents realized service capacity.

---

### 3. Time-in-System Proxy (Little’s Law)

Using Little’s Law:

[
L = \lambda W
]

We approximate:

[
W \approx \frac{\bar{L}}{\text{throughput}}
]

This estimates average time a customer spends in the system (not pure waiting time).

---

## Utilization and Stability

For each station:

[
\rho_i = \frac{\lambda}{\mu_i}
]

* ( \rho < 1 ) → Stable system
* ( \rho \approx 1 ) → High sensitivity to variability
* ( \rho > 1 ) → Queue grows unbounded over time

In serial systems, the lowest service rate defines the bottleneck.

---

## Baseline Interpretation

The Baseline scenario represents current operational performance under:

* Average arrival rate λ
* Observed service rates μ₀, μ₁, μ₂

It serves as a reference point for evaluating operational interventions.

---

## Key Insight

Simulation results demonstrate:

* The Till stage often acts as the primary bottleneck.
* Small improvements in Till service rate significantly reduce overall queue length.
* Improvements at downstream stages (Shots, Milk) yield smaller marginal effects when Till remains constrained.

This reflects classical queueing theory behavior in high-utilization serial systems.

---

## Model Limitations

This base model assumes:

* Constant arrival rate (no time-of-day variation)
* No menu-dependent service time variation
* No learning curve effects
* No customer abandonment (balking/reneging)
* Single server per stage

The model is intentionally simplified to isolate structural bottlenecks.

---

## Purpose

This simulation is not intended to perfectly replicate operational reality.

Instead, it provides:

* A structural lens to understand congestion dynamics
* A quantitative framework for bottleneck analysis
* A foundation for future extensions (time-varying demand, learning curves, healthcare analogs)

---

If you'd like, I can now help you write:

* A strong **Project Motivation** section (linking this to systems thinking and healthcare ops), or
* A concise **Executive Summary** for recruiters, or
* A more technical appendix explaining the mathematics in greater depth.
