# Utilization Analysis: The Fundamental Queueing Law

## Motivation

In all queueing systems, there is a fundamental nonlinear relationship between
**utilization** (ρ) and **congestion** (average queue length L̄).

This section explores that relationship by sweeping utilization from ρ=0.2 to
ρ=0.95 while holding all service rates constant (μ₀=65, μ₁=85, μ₂=75) and
varying arrival rate λ.

## Definition

Utilization at the Till stage:

```
ρ = λ / μ₀
```

Where λ is the arrival rate (customers/hour) and μ₀ is the till service rate.

## Results

The following table shows how average system queue length L̄ behaves as
utilization increases.

| ρ (Utilization) | λ (arrivals/hr) | L̄ (avg queue) | Throughput (orders/hr) | W (wait min) |
|-----------------|-----------------|----------------|------------------------|--------------|
| 0.20            | 13.0            | 0.55           | 13.02                  | ~2.5         |
| 0.30            | 19.5            | 0.94           | 19.47                  | ~2.9         |
| 0.40            | 26.0            | 1.46           | 25.89                  | ~3.4         |
| 0.50            | 32.5            | 2.13           | 32.34                  | ~4.0         |
| 0.60            | 39.0            | 3.10           | 38.65                  | ~4.8         |
| 0.70            | 45.5            | 4.60           | 45.13                  | ~6.1         |
| 0.80            | 52.0            | 7.12           | 51.34                  | ~8.3         |
| 0.85            | 55.2            | 9.21           | 54.23                  | ~10.2        |
| 0.90            | 58.5            | 12.15          | 56.86                  | ~12.9        |
| 0.95            | 61.8            | 16.69          | 58.94                  | ~17.1        |

## Key Observations

### 1. **Non-linear relationship**
Queue length does NOT grow linearly with ρ. Instead:
- ρ = 0.2–0.6: L̄ grows slowly (0.55 → 3.10)
- ρ = 0.6–0.8: L̄ accelerates (3.10 → 7.12)
- ρ = 0.8–0.95: L̄ steepens dramatically (7.12 → 16.69)

### 2. **The "knee" occurs around ρ ≈ 0.75–0.85**
Below this zone, the system is stable and predictable.  
Above this zone, small changes in arrival rate produce large increases in
wait time. This is the **critical utilization range**.

### 3. **Exponential behavior near saturation**
As ρ → 1, queue lengths grow without bound. This is a fundamental property
of M/M/1 queues, well-known in queueing theory.

### 4. **Implication for operations**
- If ρ < 0.7, the queue is manageable and relatively insensitive to small
  demand variations.
- If ρ > 0.85, the system is in a **dangerous zone** where tiny increases in
  demand can cause service collapse.

## Operational Insight

This curve illustrates why **buffering against demand variation is critical**
in high-utilization systems. A shop designed for ρ = 0.8 will experience
dramatically different customer experience on days when demand pushes
toward ρ = 0.9.

Real-world decisions:
- Target ρ ≤ 0.7 for predictability
- Use staffing to modulate ρ (more servers = lower ρ)
- Use preorder / buffer policies to smooth demand

## Mathematical Context

The theoretical M/M/1 queue predicts:

```
L = ρ / (1 − ρ)
```

Our simulation should approximate this curve, confirming that the three-stage
serial model exhibits classic queueing behavior at the aggregate level.

## Next

- Compare simulation results against theoretical M/M/1 formula
- Test whether multiserver (M/M/c) exhibits the same nonlinearity
- Explore how menu-dependent service times affect this curve
