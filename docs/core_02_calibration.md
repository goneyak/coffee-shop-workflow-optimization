# Calibration Notes (λ, μ in Real Units)

## Goal
Connect model parameters (λ, μ0, μ1, μ2) to realistic business signals.

## Unit sanity
- λ: customers/hour
- μ: customers/hour per station
- L̄: average number of customers in-system (count)
- W: hours (convert to minutes)

## Back-of-envelope approach (example)
If daily revenue ≈ 4000€ and average basket ≈ 6.5€:
- Orders/day ≈ 4000/6.5 ≈ 615
If shop is open 8 hours:
- λ ≈ 615/8 ≈ 77 orders/hour

## What still needs measurement (TODO)
- % drinks vs food orders
- average till handling time distribution
- drink mix (milk drinks vs espresso-only vs matcha/hot chocolate)
- # active servers per station by time-of-day

## Next
- Peak arrivals and visible queue metrics