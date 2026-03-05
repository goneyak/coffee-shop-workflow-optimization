# Project Map (Coffee Shop Workflow Optimization)

## What exists today
- Base model: Arrival → Till → Shots → Milk → Exit
- Discrete-time stochastic simulation
- Scenario comparisons via μ changes
- Output: results/*/summary.csv

## How to navigate this repo
- `README.md`: portfolio overview + headline results
- `src/`: simulation + experiments + plotting code
- `configs/`: experiment settings (reproducible runs)
- `results/`: experiment outputs (csv + figures)
- `docs/`: extension notes (design decisions + math + interpretations)

## Extensions roadmap
1. Base model definition (docs/01_base_model.md)
2. Calibration from business numbers (docs/02_calibration.md)
3. Peak arrivals (docs/03_peak_arrivals.md)
4. Visible queue vs system backlog (docs/04_visible_queue.md)
5. Preorder / pipeline policy (docs/05_preorder_buffer.md) *(implemented as Scenario 5)*
6. Multi-server Till staffing (docs/06_multi_server.md) *(implemented as Scenario 6)*
7. Utilization sweep analysis (docs/07_utilization_analysis.md) *(implemented)*
8. Menu-dependent service times (docs/08_menu_dependent_service.md)
9. Healthcare ops mapping (docs/09_healthcare_mapping.md)