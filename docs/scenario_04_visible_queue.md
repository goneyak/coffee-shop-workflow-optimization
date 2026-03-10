# Scenario 4 - Visible Queue vs System Backlog

## Motivation
Customers perceive the "line" mainly at Till, while operations suffer from hidden backlog at bar stages.

## Modeling change
Track:
- Visible queue: q0
- Bar backlog: q1 + q2
- Total WIP: q0 + q1 + q2

## Implementation plan
- Output additional metrics in simulation result:
  - avg_q0, avg_q1, avg_q2
  - peak_q0, peak_total
- Add plots comparing q0 vs total

## Experiments (Completed)
- Peak arrivals scenario with detailed queue breakdown
- Results: `results/visible_queue/summary.csv`

## Results
| Queue Component | Average Length | Peak Length | % of Total |
|----------------|----------------|-------------|-----------|
| **Visible Queue (Till)** | 46.3 | 157 | 88.8% |
| **Bar Backlog (Shots)** | 2.2 | - | 4.2% |
| **Bar Backlog (Milk)** | 3.7 | - | 7.0% |
| **Total System** | 52.1 | 167 | 100% |

## Interpretation
During lunch rush:
- Customers see ~46 people waiting at Till
- But system has 52 orders in progress
- About 6 orders are "invisible" work behind the bar
- Peak visible queue reaches ~157 customers

This explains why baristas feel overwhelmed even when the visible line seems manageable.

## Visualization

![Peak Arrivals Queue Over Time](../results/peak_arrivals_queue_plot.png)

Related result file:
- `results/visible_queue/summary.csv`

## Next
- Multi-server staffing at Till
- Explore interplay with pipeline/preorder policy (see docs/scenario_05_preorder_buffer.md)