import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Power constraints
p_grid_max, p_grid_min = 10, -10
p_BEV_max, p_BEV_min = 100, 50
p_BES_max, p_BES_min = 100, 50
p_PHEV_max, p_PHEV_min = 100, 50
p_DIG_max, p_DIG_min = 100, 0

# Cost and capacity constraints
bid_grid = 20
CTCPD = 1500
c_max, c_min = 500, 50

# Simulated annealing parameters
T = 1000000
T_initial = 0.0001
beta = (T - T_initial) / 1000

def get_random_power(power_min, power_max):
    return random.randint(power_min, power_max)


def get_random_capacity(c_min, c_max):
    return random.randint(c_min, c_max)


def calculate_cost_grid(p_grid):
    return abs(20 * p_grid) if p_grid > 0 else abs((1 - 0.1) * 20 * p_grid)


def calculate_diesel_cost(p_grid):
    return abs(p_grid ** 3 * 10)


def calculate_total_cost(p_grid, p_bes, p_phev, p_bev, cost_grid, diesel_cost, capacity):
    ct = 20 * (abs(p_grid) + p_bes + p_phev + p_bev) + cost_grid
    diesel_price = 10 * (diesel_cost + capacity)
    return ct + diesel_price + CTCPD


e = -1
while e < 0:
    P_grid = get_random_power(p_grid_min, p_grid_max)
    P_BEV = get_random_power(p_BEV_min, p_BEV_max)
    P_BES = get_random_power(p_BES_min, p_BES_max)
    P_PHEV = get_random_power(p_PHEV_min, p_PHEV_max)
    P_DIG = get_random_power(p_DIG_min, p_DIG_max)

    costGrid = calculate_cost_grid(P_grid)
    dieselCost = calculate_diesel_cost(P_grid)
    capacity = get_random_capacity(c_min, c_max)
    e = calculate_total_cost(P_grid, P_BES, P_PHEV, P_BEV, costGrid, dieselCost, capacity)


xplot, yplot = np.zeros(1000), np.zeros(1000)
iteration = 0

p_grid1, p_bev1, p_bes1, p_phev1, p_dig1 = P_grid, P_BEV, P_BES, P_PHEV, P_DIG
e3 = e

while iteration < 1000:
    costGrid1 = calculate_cost_grid(p_grid1)
    dieselCost1 = calculate_diesel_cost(p_grid1)
    capacity1 = get_random_capacity(c_min, c_max)
    e1 = calculate_total_cost(p_grid1, p_bes1, p_phev1, p_bev1, costGrid1, dieselCost1, capacity1)

    y = -1
    while y < 0:
        x1 = 0.03 * random.randint(-10, 10)

        p_grid2 = np.clip(p_grid1 + x1, p_grid_min, p_grid_max)
        p_bev2 = np.clip(p_bev1 + x1, p_BEV_min, p_BEV_max)
        p_bes2 = np.clip(p_bes1 + x1, p_BES_min, p_BES_max)
        p_phev2 = np.clip(p_phev1 + x1, p_PHEV_min, p_PHEV_max)
        p_dig2 = np.clip(p_dig1 + x1, p_DIG_min, p_DIG_max)

        costGrid2 = calculate_cost_grid(p_grid2)
        dieselCost2 = calculate_diesel_cost(p_grid2)
        capacity2 = get_random_capacity(c_min, c_max)
        e2 = calculate_total_cost(p_grid2, p_bes2, p_phev2, p_bev2, costGrid2, dieselCost2, capacity2)

        y = e2

    delta_E = (e2 - e1) / 100
    if e2 < e1 or math.exp(-delta_E / T) > random.random():
        p_grid1, p_bev1, p_bes1, p_phev1, p_dig1 = p_grid2, p_bev2, p_bes2, p_phev2, p_dig2
        e1 = e2
    
    T -= beta * iteration
    
    if e3 > e1:
        e3 = e1
    
    xplot[iteration], yplot[iteration] = iteration, e3
    iteration += 1

print(f'Pgrid={p_grid1} Pbes={p_bes1} Pbev={p_bev1} Pphev={p_phev1} Pdig={p_dig1} Cost={e3}')
plt.plot(xplot, yplot)
plt.show()

# This version simplifies the structure, removes redundant classes, and optimizes value adjustments! 🚀
