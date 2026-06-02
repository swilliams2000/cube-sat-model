import numpy as np
import matplotlib.pyplot as plt

# =========================
# MISSION PARAMETERS
# =========================
days = 365
orbits_per_day = 15  # ~95 min orbit
total_orbits = days * orbits_per_day

dt_orbit = 1  # orbit-level timestep

# =========================
# INITIAL SYSTEM PARAMETERS
# =========================
solar_flux = 1361
area = 0.06
efficiency = 0.28
system_loss = 0.90

battery_capacity_Wh = 20
battery_energy = 0.8 * battery_capacity_Wh

# degradation assumptions (realistic)
solar_degradation_rate = 0.0005  # ~0.05% per orbit (~~15%/year)
battery_degradation_rate = 0.0002

# =========================
# STORAGE
# =========================
soc = []
solar_history = []
load_history = []
orbit_index = []

# =========================
# LOAD MODEL (same logic, orbit-based)
# =========================
def get_load(orbit):
    base = 6  # OBC + ADCS + idle comms

    # periodic comms every 5 orbits
    if orbit % 5 == 0:
        comms = 8
    else:
        comms = 0.5

    # payload every 20 orbits
    if orbit % 20 == 0:
        payload = 5
    else:
        payload = 0

    return base + comms + payload

# =========================
# SOLAR MODEL
# =========================
def solar_power(orbit, degraded_efficiency):
    # simple seasonal/orbit variation (beta angle proxy)
    angle_factor = 0.7 + 0.3 * np.sin(orbit / 50)

    P_max = solar_flux * area * degraded_efficiency * system_loss

    return P_max * angle_factor

# =========================
# SIMULATION LOOP (FULL YEAR)
# =========================
for orbit in range(total_orbits):

    # degrade system over time
    eff = efficiency * (1 - solar_degradation_rate * orbit)

    batt_capacity = battery_capacity_Wh * (1 - battery_degradation_rate * orbit)

    solar = solar_power(orbit, eff)

    load = get_load(orbit)

    # assume orbit-averaged sunlight fraction (~0.65)
    sun_fraction = 0.65

    solar_energy = solar * sun_fraction
    load_energy = load  # per orbit average W ~ Wh per orbit unitized

    net = (solar_energy - load_energy)

    # battery update
    if net > 0:
        battery_energy += net * 0.92
    else:
        battery_energy += net / 0.92

    # clamp
    battery_energy = max(0, min(batt_capacity, battery_energy))

    # store
    soc.append(battery_energy)
    solar_history.append(solar_energy)
    load_history.append(load_energy)
    orbit_index.append(orbit)

# =========================
# RESULTS
# =========================
time_days = np.array(orbit_index) / orbits_per_day

plt.figure(figsize=(12,6))

plt.plot(time_days, soc, label="Battery SOC (Wh)")
plt.xlabel("Mission Time (Days)")
plt.ylabel("Battery Energy (Wh)")
plt.title("3U CubeSat Full-Year Power Simulation (EOL + Degradation)")
plt.grid()
plt.legend()

plt.show()

# =========================
# METRICS
# =========================
print("Max Battery:", max(soc))
print("Min Battery:", min(soc))
print("End Battery:", soc[-1])

# failure detection
if min(soc) <= 0:
    print("⚠️ MISSION FAILURE: Battery depletion occurred")
else:
    print("✅ Mission survives full year under assumptions")