# Simulation configuration

SIM_TIME_HOURS = 8
DT = 0.005 
RUNS = 300

ARRIVAL_RATE = 60

SCENARIOS = {
    "Baseline": {
        "mu0": 65,   # Till
        "mu1": 85,   # Shots
        "mu2": 75    # Milk
    },
    "Improved_Till_Training": {
        "mu0": 75,
        "mu1": 85,
        "mu2": 75
    },
    "Full_Improvement": {
        "mu0": 75,
        "mu1": 95,
        "mu2": 85
    }
}