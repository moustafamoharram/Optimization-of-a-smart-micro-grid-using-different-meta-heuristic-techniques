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

# Generate initial solutions
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

# Initialize teacher and students
p_teacher, p_student1, p_student2, p_student3, p_student4 = solutions[:5]

# Optimization loop
xplot, yplot = np.zeros(10000), np.zeros(10000)
for i in range(10000):
    # Calculate mean values
    p_grid_mean = (p_teacher[0] + p_student1[0] + p_student2[0] + p_student3[0] + p_student4[0]) / 5
    p_bev_mean = (p_teacher[1] + p_student1[1] + p_student2[1] + p_student3[1] + p_student4[1]) / 5
    p_bes_mean = (p_teacher[2] + p_student1[2] + p_student2[2] + p_student3[2] + p_student4[2]) / 5
    p_phev_mean = (p_teacher[3] + p_student1[3] + p_student2[3] + p_student3[3] + p_student4[3]) / 5
    p_dig_mean = (p_teacher[4] + p_student1[4] + p_student2[4] + p_student3[4] + p_student4[4]) / 5

    # Update student 1
    a = random.random()
    tf = random.randint(1, 2)
    s10 = p_student1[0] + a * (p_teacher[0] - (tf * p_grid_mean))
    s11 = p_student1[1] + a * (p_teacher[1] - (tf * p_bev_mean))
    s12 = p_student1[2] + a * (p_teacher[2] - (tf * p_bes_mean))
    s13 = p_student1[3] + a * (p_teacher[3] - (tf * p_phev_mean))
    s14 = p_student1[4] + a * (p_teacher[4] - (tf * p_dig_mean))

    # Ensure constraints
    s10 = max(min(s10, p_grid_max), p_grid_min)
    s11 = max(min(s11, p_BEV_max), p_BEV_min)
    s12 = max(min(s12, p_BES_max), p_BES_min)
    s13 = max(min(s13, p_PHEV_max), p_PHEV_min)
    s14 = max(min(s14, p_DIG_max), p_DIG_min)

    s15 = calculate_total_cost(s10, s11, s12, s13, s14, bb2)

    # Update student 2
    a = random.random()
    tf = random.randint(1, 2)
    s20 = p_student2[0] - a * (p_teacher[0] - (tf * p_grid_mean))
    s21 = p_student2[1] - a * (p_teacher[1] - (tf * p_bev_mean))
    s22 = p_student2[2] - a * (p_teacher[2] - (tf * p_bes_mean))
    s23 = p_student2[3] - a * (p_teacher[3] - (tf * p_phev_mean))
    s24 = p_student2[4] - a * (p_teacher[4] - (tf * p_dig_mean))

    # Ensure constraints
    s20 = max(min(s20, p_grid_max), p_grid_min)
    s21 = max(min(s21, p_BEV_max), p_BEV_min)
    s22 = max(min(s22, p_BES_max), p_BES_min)
    s23 = max(min(s23, p_PHEV_max), p_PHEV_min)
    s24 = max(min(s24, p_DIG_max), p_DIG_min)

    s25 = calculate_total_cost(s20, s21, s22, s23, s24, bb2)

    # Update student 3
    a = random.random()
    tf = random.randint(1, 2)
    s30 = p_student3[0] - a * (p_teacher[0] - (tf * p_grid_mean))
    s31 = p_student3[1] - a * (p_teacher[1] - (tf * p_bev_mean))
    s32 = p_student3[2] - a * (p_teacher[2] - (tf * p_bes_mean))
    s33 = p_student3[3] - a * (p_teacher[3] - (tf * p_phev_mean))
    s34 = p_student3[4]