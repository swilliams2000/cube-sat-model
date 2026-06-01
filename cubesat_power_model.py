import numpy as np
import matplotlib.pyplot as plt

# =========================
# ORBIT PARAMETERS
# =========================
orbit_period_min = 95
dt = 1  # minute resolution
t = np.arange(0, orbit_period_min, dt)

sunlight_duration = 60  # min
eclipse_duration = orbit_period_min - sunlight_duration

# =========================
# SOLAR ARRAY MODEL
# =========================
solar_flux = 1361  # W/m^2
area = 0.06  # m^2 (3U body-mounted estimate)
efficiency = 0.28
degradation = 0.80
system_loss = 0.90

P_max = solar_flux * area * efficiency * degradation * system_loss

# =========================
# BATTERY MODEL
# =========================
battery_capacity_Wh = 20
battery_energy = 0.8 * battery_capacity_Wh
battery_efficiency = 0.92

# =========================
# LOAD MODEL (REALISTIC MODES)
# =========================

def in_sunlight(time):
    return time < sunlight_duration

def get_load(time):
    # Always-on systems
    base = 2 + 3 + 1  # OBC + ADCS + idle comms

    # Communication window
    if 20 <= time < 35:
        comms = 8
    else:
        comms = 0.5

    # Payload duty cycle
    if 50 <= time < 55:
        payload = 5
    else:
        payload = 0

    return base + comms + payload

# =========================
# SOLAR INCIDENCE MODEL
# =========================
def solar_incidence_factor(time):
    if not in_sunlight(time):
        return 0

    # simple cosine variation over sunlight period
    angle = (time / sunlight_duration) * np.pi
    return max(0, np.cos(angle))

# =========================
# STORAGE
# =========================
soc = []
solar_trace = []
load_trace = []

# =========================
# SIMULATION LOOP
# =========================
for i in t:

    if in_sunlight(i):
        solar = P_max * solar_incidence_factor(i)
    else:
        solar = 0

    load = get_load(i)

    # energy over timestep (Wh)
    net = (solar - load) * (dt / 60)

    # battery update with efficiency
    if net > 0:
        battery_energy += net * battery_efficiency
    else:
        battery_energy += net / battery_efficiency

    # clamp
    battery_energy = max(0, min(battery_capacity_Wh, battery_energy))

    soc.append(battery_energy)
    solar_trace.append(solar)
    load_trace.append(load)

# =========================
# RESULTS
# =========================
plt.figure(figsize=(10,6))

plt.plot(t, soc, label="Battery SOC (Wh)")
plt.plot(t, solar_trace, label="Solar Power (W)")
plt.plot(t, load_trace, label="Load Power (W)")

plt.xlabel("Time (minutes)")
plt.title("3U CubeSat Power Simulation (Realistic Model)")
plt.grid()
plt.legend()

plt.show()

# =========================
# METRICS
# =========================
print("Max Battery:", max(soc))
print("Min Battery:", min(soc))
print("End Battery:", soc[-1])