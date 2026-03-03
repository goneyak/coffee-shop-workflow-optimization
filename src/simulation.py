import numpy as np

def simulate(arrival_rate, mu0, mu1, mu2, sim_time_hours, dt, seed=None):

    if seed is not None:
        np.random.seed(seed)

    steps = int(sim_time_hours / dt)

    q0 = 0  # Till
    q1 = 0  # Shots
    q2 = 0  # Milk

    completed = 0
    total_queue = 0
    queue_series = []

    for _ in range(steps):

        # 1. arrivals
        arrivals = np.random.poisson(arrival_rate * dt)
        q0 += arrivals

        # 2. Till service
        service0 = np.random.poisson(mu0 * dt)
        served0 = min(q0, service0)
        q0 -= served0
        q1 += served0

        # 3. Shots service
        service1 = np.random.poisson(mu1 * dt)
        served1 = min(q1, service1)
        q1 -= served1
        q2 += served1

        # 4. Milk service
        service2 = np.random.poisson(mu2 * dt)
        served2 = min(q2, service2)
        q2 -= served2
        completed += served2

        total_queue += (q0 + q1 + q2)
        queue_series.append(q0 + q1 + q2)

    avg_queue_length = total_queue / steps
    throughput = completed / sim_time_hours

    return {
        "avg_queue_length": avg_queue_length,
        "throughput": throughput,
        "completed": completed,
        "queue_series": queue_series
    }