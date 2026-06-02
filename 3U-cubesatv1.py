import numpy as np
import matplotlib.pyplot as plt

# =====================================
# MISSION PARAMETERS
# =====================================

MISSION_DAYS = 365

# =====================================
# SOLAR SYSTEM
# =====================================

SOLAR_FLUX = 1361  # W/m²

solar_area = 0.06      # m²
solar_eff = 0.28
system_eff = 0.90

initial_solar_power = (
    SOLAR_FLUX *
    solar_area *
    solar_eff *
    system_eff
)

# =====================================
# BATTERY
# =====================================

initial_battery_capacity = 20.0  # Wh

battery_energy = 16.0  # start at 80%

# =====================================
# LOADS
# =====================================

average_load = 8.0  # W

# =====================================
# ORBITAL ASSUMPTIONS
# =====================================

orbits_per_day = 15

sunlight_hours_per_orbit = 60 / 60
eclipse_hours_per_orbit = 35 / 60

sunlight_hours_per_day = (
    sunlight_hours_per_orbit *
    orbits_per_day
)

# =====================================
# STORAGE
# =====================================

days = []
soc = []

# =====================================
# DAILY SIMULATION
# =====================================

for day in range(MISSION_DAYS):

    # Solar degradation
    solar_degradation = 1 - 0.20 * (day / MISSION_DAYS)

    # Battery degradation
    battery_capacity = (
        initial_battery_capacity *
        (1 - 0.15 * (day / MISSION_DAYS))
    )

    # Seasonal illumination variation
    seasonal_factor = (
        0.9 +
        0.1 * np.sin(
            2 * np.pi * day / 365
        )
    )

    solar_power = (
        initial_solar_power *
        solar_degradation *
        seasonal_factor
    )

    # Daily energy generated
    energy_generated = (
        solar_power *
        sunlight_hours_per_day
    )

    # Daily energy consumed
    energy_consumed = (
        average_load *
        24
    )

    net_energy = (
        energy_generated -
        energy_consumed
    )

    battery_energy += net_energy

    battery_energy = max(
        0,
        min(
            battery_capacity,
            battery_energy
        )
    )

    days.append(day)
    soc.append(battery_energy)

# =====================================
# RESULTS
# =====================================

plt.figure(figsize=(12,6))

plt.plot(days, soc)

plt.title(
    "3U CubeSat Battery State of Charge Over 1 Year"
)

plt.xlabel("Mission Day")
plt.ylabel("Battery Energy (Wh)")
plt.grid()

plt.show()

# =====================================
# METRICS
# =====================================

print("\n===== RESULTS =====")
print(f"Initial SOC: {soc[0]:.2f} Wh")
print(f"Final SOC:   {soc[-1]:.2f} Wh")
print(f"Minimum SOC: {min(soc):.2f} Wh")

if min(soc) <= 0:
    print("❌ Mission failed")
else:
    print("✅ Mission survived")