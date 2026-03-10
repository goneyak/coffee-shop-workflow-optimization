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
- `docs/README.md`: canonical doc index + archive notes

## Extensions roadmap
1. Scenario 1 - Improved Till efficiency (docs/scenario_01_improved_till.md)
2. Scenario 2 - Full workflow improvement (docs/scenario_02_full_improvement.md)
3. Peak arrivals (docs/scenario_03_peak_arrivals.md)
4. Visible queue vs system backlog (docs/scenario_04_visible_queue.md)
5. Preorder / pipeline policy (docs/scenario_05_preorder_buffer.md) *(implemented as Scenario 5)*
6. Multi-server Till staffing (docs/scenario_06_multi_server.md) *(implemented as Scenario 6)*
7. Utilization sweep analysis (docs/core_03_utilization_analysis.md) *(implemented)*
8. Menu-dependent service times (docs/scenario_07_menu_dependent_service.md) *(implemented as Scenario 7)*
9. Healthcare ops mapping (docs/scenario_08_healthcare_mapping.md) *(implemented as Scenario 8)*

## Archive note
- `docs/archive_multi_server_draft.md` is an archived draft.
- Use `docs/scenario_06_multi_server.md` as the canonical multi-server documentation.