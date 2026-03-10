# Executive Summary (One Page)

## Project Question
Are delays caused by individual performance, or by workflow structure under high utilization?

## Evaluation Metrics
- `avgQ`: Average work-in-progress in system (q0 + q1 + q2)
- `thr`: Throughput (orders/hour)
- `wait`: Estimated average time in system (minutes)
- `Bottleneck signal`: Stage with largest queue pressure (q0/q1/q2)

## Scenario Results Snapshot (Latest)

| Scenario | avgQ | thr (/h) | wait (min) | Bottleneck signal | Operational interpretation |
|---|---:|---:|---:|---|---|
| Baseline | 14.05 | 57.90 | 14.56 | q0 dominant | Till is the primary queue source in base operations |
| S1 Improved Till | 9.61 | 59.03 | 9.77 | q0 sharply reduced | Front-stage process fixes produce immediate queue relief |
| S2 Full Improvement | 7.24 | 59.01 | 7.36 | q0/q1/q2 all reduced | End-to-end acceleration cuts delay, throughput gain remains bounded |
| S3 Peak Arrivals | 51.15 | 54.02 | 56.81 | extreme q0 + peak total | Demand spikes cause waiting explosion more than throughput gain |
| S4 Visible Queue | 52.11 | 54.09 | 57.80 | q0 visible, q1+q2 hidden | Customer-visible line underestimates true internal WIP |
| S5 Preorder (small) | 12.70 | 57.90 | 13.16 | q1 reduced (not zero) | Limited priority buffer smooths middle stage partially |
| S5 Preorder (large) | 12.02 | 57.90 | 12.46 | q1 near zero | Larger priority buffer redistributes queue more effectively |
| S6 Multi-server till (2) | 6.64 | 59.32 | 6.72 | q0 collapses, q2 remains | Second till gives the biggest staffing ROI |
| S6 Multi-server till (3) | 6.14 | 59.40 | 6.20 | downstream stages become binding | Third till gives diminishing returns |
| S7 Menu quick | 10.46 | 72.14 | 8.70 | q1 increases | Fast menu mix boosts throughput but can stress shots stage |
| S7 Menu milk-heavy | 12.68 | 71.24 | 10.68 | q2 increases | Milk-heavy mix shifts pressure downstream |
| S8 Healthcare baseline | 10.05 | 25.20 | 23.92 | q2 highest | Downstream treatment capacity dominates delay |
| S8 Healthcare peak ED | 15.19 | 25.41 | 35.87 | q1/q2 surge | Peak demand worsens waiting with minor throughput change |
| S8 Healthcare extra triage | 13.66 | 25.52 | 32.10 | q0 down, q1/q2 still high | Front-door staffing helps perception but not full-system delay |

## Cross-Scenario Conclusions
1. Queue reduction is often easier than throughput increase in serial systems.
2. The biggest gains come from relieving the active bottleneck, not uniformly speeding every stage.
3. Under peak demand, waiting grows nonlinearly; spare capacity is a strategic requirement.
4. Policies like preorder primarily redistribute congestion unless downstream capacity also improves.
5. The same queueing logic transfers to healthcare and other service operations.

## Practical Recommendation Order
1. Add second till server (high impact, low modeling uncertainty).
2. Improve till process friction (POS, loyalty flow, customization handling).
3. Use preorder buffer with explicit capacity limits.
4. Match staffing and prep design to menu mix by time-of-day.
5. For healthcare analogs, pair triage interventions with downstream diagnostics/treatment capacity.

## Source Files
- Coffee scenarios: `results/*/summary.csv`
- Utilization curve: `results/utilization_summary.csv`
- Key visuals: `results/scenario_comparison.png`, `results/multi_server_lineplot.png`, `results/menu_timeseries_comparison.png`, `results/healthcare_comparison.png`
