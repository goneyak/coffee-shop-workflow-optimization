# Extension: Visible Queue vs System Backlog

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
| **Visible Queue (Till)** | 45.5 | 155 | 89% |
| **Bar Backlog (Shots)** | 2.1 | - | 4% |
| **Bar Backlog (Milk)** | 3.6 | - | 7% |
| **Total System** | 51.1 | 165 | 100% |

## Interpretation
During lunch rush:
- Customers see ~45 people waiting at Till
- But system has 51 orders in progress
- 6 orders are "invisible" work behind the bar
- Peak visible queue reaches 155 customers

This explains why baristas feel overwhelmed even when the visible line seems manageable.

## Next
- Multi-server staffing at Till
- Explore interplay with pipeline/preorder policy (see docs/05_preorder_buffer.md)