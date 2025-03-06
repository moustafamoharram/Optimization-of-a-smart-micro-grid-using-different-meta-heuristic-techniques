import random
import numpy as np
import matplotlib.pyplot as plt

# Constants
p_grid_max, p_grid_min = 10, -10
p_BEV_max, p_BEV_min = 100, 50
p_BES_max, p_BES_min = 100, 50
p_PHEV_max, p_PHEV_min = 100, 50
p_DIG_max, p_DIG_min = 100, 0
cost_BEV, cost_BES, cost_PHEV = 100, 150, 200
bid_grid, CTCPD, cf = 20, 1500, 10
c_max, c_min = 500, 50

# Methods
def get_power(power_min, power_max):
    return random.randint(power_min, power_max)

def get_battery_capacity(c_min, c_max):
    return random.randint(c_min, c_max)

def get_cost_grid(p_grid):
    if p_grid > 0:
        return abs(20 * p_grid)
    elif p_grid < 0:
        return abs((1 - 0.1) * 20 * p_grid)
    else:
        return 0

def get_cost_diesel(p_grid):
    return abs(p_grid ** 3 * 10)

def calculate_total_cost(p_grid, p_BEV, p_BES, p_PHEV, p_DIG, bb2):
    cost_grid = get_cost_grid(p_grid)
    ct = 20 * (p_grid + p_BES + p_PHEV + p_BEV) + cost_grid
    dd = get_cost_diesel(p_grid)
    diesel_price = 10 * (dd + bb2)
    return ct + diesel_price + CTCPD

# Main logic
bb2 = get_battery_capacity(c_min, c_max)
solutions = []

for _ in range(5):
    while True:
        P_grid = get_power(p_grid_min, p_grid_max)
        P_BEV = get_power(p_BEV_min, p_BEV_max)
        P_BES = get_power(p_BES_min, p_BES_max)
        P_PHEV = get_power(p_PHEV_min, p_PHEV_max)
        P_DIG = get_power(p_DIG_min, p_DIG_max)
        total_cost = calculate_total_cost(P_grid, P_BEV, P_BES, P_PHEV, P_DIG, bb2)
        if total_cost >= 0:
            solutions.append((P_grid, P_BEV, P_BES, P_PHEV, P_DIG, total_cost))
            break

# Sort solutions by total cost
solutions.sort(key=lambda x: x[5])

# Initialize elite solutions
elite, p1, p2, p3, worst = solutions[:5]

# Optimization loop
xplot, yplot = np.zeros(500), np.zeros(500)
for i in range(500):
    # Mutation
    x1 = random.randint(-10, 10)
    for _ in range(1):
        if worst[0] + x1 < p_grid_max and worst[0] + x1 > p_grid_min:
            worst = (worst[0] + x1, *worst[1:])
        if worst[1] + x1 < p_BEV_max and worst[1] + x1 > p_BEV_min:
            worst = (worst[0], worst[1] + x1, *worst[2:])
        if worst[4] + x1 < p_DIG_max and worst[4] + x1 > p_DIG_min:
            worst = (*worst[:4], worst[4] + x1, worst[5])

    # Recalculate costs
    elite_cost = calculate_total_cost(*elite[:5], bb2)
    p1_cost = calculate_total_cost(*p1[:5], bb2)
    p2_cost = calculate_total_cost(*p2[:5], bb2)
    p3_cost = calculate_total_cost(*p3[:5], bb2)
    worst_cost = calculate_total_cost(*worst[:5], bb2)

    # Update solutions
    solutions = [elite, p1, p2, p3, worst]
    solutions.sort(key=lambda x: x[5])
    elite, p1, p2, p3, worst = solutions[:5]

    # Record the best cost
    xplot[i] = i
    yplot[i] = elite[5]

    # Crossover
    rr = random.randint(0, 4)
    p1 = list(p1)
    p1[rr] = elite[rr] * 0.9
    p1 = tuple(p1)

    rr = random.randint(0, 4)
    p2 = list(p2)
    p2[rr] = elite[rr] * 0.9
    p2 = tuple(p2)

    rr = random.randint(0, 4)
    p3 = list(p3)
    if random.randint(0, 1) == 0:
        p3[rr] = elite[rr] * 0.9
    else:
        p3[rr] = p1[rr] * 0.9
    p3 = tuple(p3)

# Output the best solution
print('Pgrid=', elite[0], ' Pbes=', elite[2], 'Pbev=', elite[1], 'Pphev=', elite[3], 'Pdig=', elite[4], 'Cost=', elite[5])

# Plot the results
plt.plot(xplot, yplot)
plt.show()