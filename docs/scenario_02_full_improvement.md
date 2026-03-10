# Scenario 2: Full Workflow Improvement

## Objective
Test a broader intervention where service rates are increased across Till, Shots, and Milk together.

## Configuration
- Baseline reference: `configs/baseline.yaml`
- Intervention: `configs/full_improvement.yaml`
- Core change: increase `mu0`, `mu1`, and `mu2`

## Result Summary (300 runs)
| Metric | Baseline | Full Improvement | Change |
|--------|----------|------------------|--------|
| Avg queue L̄ | 14.05 | 7.24 | -48.5% |
| Throughput (orders/hr) | 57.90 | 59.01 | +1.92% |
| Estimated wait (min) | 14.6 | 7.4 | -49.3% |

## Interpretation
- End-to-end service acceleration almost halves in-system congestion.
- Throughput gain remains modest because the system is already near its practical ceiling in this setup.
- Compared with Scenario 1, this strategy adds implementation complexity but gives extra delay reduction.

## Related Artifacts
- Config: `configs/full_improvement.yaml`
- Results: `results/full_improvement/summary.csv`
- Cross-scenario comparison: `results/scenario_comparison.png`

## Visualization

![Scenario Comparison](../results/scenario_comparison.png)
