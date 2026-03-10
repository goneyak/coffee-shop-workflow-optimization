# Scenario 1: Improved Till Efficiency

## Objective
Evaluate how much congestion can be reduced by improving the ordering/payment stage (Till) without changing downstream bar capacity.

## Configuration
- Baseline reference: `configs/baseline.yaml`
- Intervention: `configs/improved_till.yaml`
- Core change: increase `mu0` (Till service rate)
- Other stages: unchanged (`mu1`, `mu2` fixed)

## Result Summary (300 runs)
| Metric | Baseline | Improved Till | Change |
|--------|----------|---------------|--------|
| Avg queue L̄ | 14.05 | 9.61 | -31.6% |
| Throughput (orders/hr) | 57.90 | 59.03 | +1.95% |
| Estimated wait (min) | 14.6 | 9.8 | -32.9% |

## Interpretation
- Upstream friction reduction delivers a large wait-time improvement.
- Throughput increases only slightly because downstream stages still cap overall capacity.
- This is a high-impact, low-disruption intervention compared with full process redesign.

## Related Artifacts
- Config: `configs/improved_till.yaml`
- Results: `results/improved_till/summary.csv`
- Cross-scenario comparison: `results/scenario_comparison.png`

## Visualization

![Scenario Comparison](../results/scenario_comparison.png)
