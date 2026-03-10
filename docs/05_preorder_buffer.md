# Extension: Preorder / Pipeline Preparation Policy

## Motivation
Customers often pay and wait at the till while baristas stand idle because the
order has not yet been released to the drinks queue. Many shops try to reduce the
visible line by allowing baristas to start drink preparation before payment is
complete – either by taking a picture of the order, using a tablet, or by simply
memorizing the next few drinks. This "preorder" or "pipeline" policy is meant
to increase concurrency without changing equipment.

## Modeling change
Introduce a priority queue that receives customers as soon as the till service
finishes. Shots staff serve that queue first, using any remaining capacity to
process the normal queue. In effect, till and shots operate in parallel rather
than strictly sequentially, though total system capacity does not change.

## Implementation notes
- Configs `preorder_buffer_small.yaml` and `preorder_buffer_large.yaml` enable
the policy.
- `src/simulation.py` now includes a `preorder_q1` counter and conditional
logic to push served customers into it and to consume it ahead of the regular
shots queue.
- `src/experiments.py` propagates `preorder_enabled` from the config to
the simulation.

## Results (Scenario 5)
Preorder reduces average system work‑in‑progress from 14.05 to 12.02 (≈14 %) and
eliminates the regular shots queue altogether (`avg_q1` drops to 0). Throughput
remains unchanged at ≈57.9 orders/hour because the milk station remains the
ultimate bottleneck.

| Scenario | mean_avg_queue | mean_throughput (/h) | mean_wait_approx (h) | mean_q0 | mean_q1 | mean_q2 |
|---|---:|---:|---:|---:|---:|---:|
| preorder_buffer_small | 12.019 | 57.897 | 0.208 | 8.714 | 0.000 | 3.306 |
| preorder_buffer_large | 12.019 | 57.897 | 0.208 | 8.714 | 0.000 | 3.306 |

Current note:
- In the current implementation and parameterization, small/large buffer
  settings produce identical aggregate KPI outputs.

## Visualization

![Scenario Comparison](../results/scenario_comparison.png)

Related result files:
- `results/preorder_buffer_small/summary.csv`
- `results/preorder_buffer_large/summary.csv`

### Takeaways
- Preorder buffering redistributes rather than removes congestion; it does not
  raise the system's capacity limit.
- The visible till line is unaffected, but baristas experience steadier work and
  clients may perceive faster service if drinks are ready when they pay.
- This pattern is most effective when accompanied by upstream capacity
  improvements (e.g. faster tills, more staff) so that the preordered queue
  itself does not become a new bottleneck.

## Next
- Compare with multi‑server tills and menu‑dependent service times to see how
  the policy interacts with other common interventions.
