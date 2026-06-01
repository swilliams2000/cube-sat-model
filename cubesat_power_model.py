import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# ASSUMED SYSTEM PARAMETERS
# ----------------------------

orbit_minutes = 90
dt = 1  # time step in minutes
time = np.arange(0, orbit_minutes, dt)

# Solar array
solar_max_power = 23  # Watts (peak in sunlight)

# Battery
battery_capacity_Wh = 20
battery_energy = 15  # start at 75%

# Loads (W)
safe_mode = 5
nominal_mode = 15
downlink_mode = 25

# Operating schedule (simple assumption)
def get_mode(t):
    if 30 <= t < 40:
        return downlink_mode
    else:
        return nominal_mode

# Sunlight vs eclipse
def in_sunlight(t):
    return t < 60  # 60 min sun, 30 min eclipse

# ----------------------------
# STORAGE
# ----------------------------
battery_history = []
solar_history = []
load_history = []

# ----------------------------
# SIMULATION LOOP
# ----------------------------
for t in time:

    # Solar power
    if in_sunlight(t):
        solar = solar_max_power
    else:
        solar = 0

    load = get_mode(t)

    # Net power
    net_power = solar - load

    # Convert W → Wh over timestep
    battery_energy += net_power * (dt / 60)

    # Clamp battery
    battery_energy = max(0, min(battery_capacity_Wh, battery_energy))

    # Store
    battery_history.append(battery_energy)
    solar_history.append(solar)
    load_history.append(load)

# ----------------------------
# PLOT RESULTS
# ----------------------------
plt.figure()

plt.plot(time, battery_history, label="Battery Energy (Wh)")
plt.plot(time, solar_history, label="Solar Power (W)")
plt.plot(time, load_history, label="Load Power (W)")

plt.xlabel("Time (minutes)")
plt.legend()
plt.title("3U CubeSat Power Model (1 Orbit)")
plt.grid()

plt.show()