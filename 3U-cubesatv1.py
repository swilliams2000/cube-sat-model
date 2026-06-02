import numpy as np
import matplotlib.pyplot as plt

# =========================
# MISSION SETUP
# =========================
DAYS = 365
ORBITS_PER_DAY = 15
TOTAL_ORBITS = DAYS * ORBITS_PER_DAY

# =========================
# CONSTANTS
# =========================
SOLAR_FLUX = 1361

# =========================
# DESIGN VARIABLES (THIS IS THE KEY DIFFERENCE)
# =========================
solar_area = 0.06        # m^2 (we will test feasibility)
battery_capacity = 20.0   # Wh

solar_eff = 0.28
system_loss = 0.90

solar_degradation = 0.20  # 20% loss over mission (EOL)
battery_degradation = 0.15 # 15% loss over mission

# =========================
# LOAD MODEL
# =========================
def load_profile(orbit):
    base = 6  # OBC + ADCS + idle comms

    # comms every 5 orbits
    comms = 8 if orbit % 5 == 0 else 0.5

    # payload every 20 orbits
    payload = 5 if orbit % 20 == 0 else 0

    return base + comms + payload

# =========================
# SOLAR MODEL
# =========================
def solar_power(orbit):
    # simple seasonal/orientation variation
    geometry_factor = 0.65 + 0.25 * np.sin(orbit / 80)

    # degrade linearly over life
    degradation_factor = 1 - solar_degradation * (orbit / TOTAL_ORBITS)

    P = SOLAR_FLUX * solar_area * solar_eff * system_loss
    return P * geometry_factor * degradation_factor

# =========================
# BATTERY STATE
# =========================
soc = 0.8 * battery_capacity

soc_history = []

min_soc = 1e9
max_soc = -1e9

failure = False

# =========================
# SIMULATION (ORBIT BY ORBIT ENERGY BALANCE)
# =========================
for orbit in range(TOTAL_ORBITS):

    # effective battery capacity decreases over time
    current_capacity = battery_capacity * (
        1 - battery_degradation * (orbit / TOTAL_ORBITS)
    )

    solar = solar_power(orbit)

    load = load_profile(orbit)

    # assume orbit average:
    sun_fraction = 0.65

    solar_energy = solar * sun_fraction
    load_energy = load

    net_energy = solar_energy - load_energy

    # battery update
    if net_energy > 0:
        soc += net_energy * 0.92
    else:
        soc += net_energy / 0.92

    # clamp
    soc = max(0, min(current_capacity, soc))

    soc_history.append(soc)

    min_soc = min(min_soc, soc)
    max_soc = max(max_soc, soc)

    # FAILURE CONDITION
    if soc <= 0:
        failure = True

# =========================
# RESULTS
# =========================
time_days = np.arange(TOTAL_ORBITS) / ORBITS_PER_DAY

plt.figure(figsize=(12,6))
plt.plot(time_days, soc_history)

plt.xlabel("Mission Time (Days)")
plt.ylabel("Battery State of Charge (Wh)")
plt.title("CubeSat Design Tool v2 — 1 Year Feasibility Check")
plt.grid()
plt.show()

# =========================
# DESIGN CHECK OUTPUT
# =========================
print("\n===== MISSION ASSESSMENT =====")
print(f"Min SOC: {min_soc:.2f} Wh")
print(f"Max SOC: {max_soc:.2f} Wh")
print(f"Final SOC: {soc:.2f} Wh")

if failure:
    print("❌ MISSION FAILURE: Battery depletion occurred")
else:
    print("✅ MISSION SUCCESS: Power-positive over full mission")

# SIMPLE DESIGN MARGIN METRIC
margin = min_soc / battery_capacity

print(f"Energy Margin: {margin:.2f}")

if margin < 0.2:
    print("⚠️ LOW MARGIN DESIGN")
elif margin < 0.4:
    print("🟡 MODERATE MARGIN")
else:
    print("🟢 ROBUST DESIGN")