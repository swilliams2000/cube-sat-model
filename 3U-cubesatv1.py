import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# MISSION PARAMETERS
# =====================================================

MISSION_DAYS = 365

ORBIT_PERIOD_MIN = 95
SUNLIGHT_MIN = 60
ECLIPSE_MIN = 35
ORBITS_PER_DAY = 15

# =====================================================
# SOLAR ARRAY
# =====================================================

SOLAR_FLUX = 1361  # W/m²

SOLAR_AREA = 0.06  # m²
CELL_EFFICIENCY = 0.28
SYSTEM_EFFICIENCY = 0.90

SOLAR_EOL_LOSS = 0.20  # 20% loss over mission

P_SOLAR_MAX = (
    SOLAR_FLUX
    * SOLAR_AREA
    * CELL_EFFICIENCY
    * SYSTEM_EFFICIENCY
)

# =====================================================
# BATTERY
# =====================================================

BATTERY_CAPACITY = 22.0  # Wh

BATTERY_EOL_LOSS = 0.15

INITIAL_SOC = 0.80

# =====================================================
# SUBSYSTEMS
# =====================================================

OBC_POWER = 1.5

ADCS_POWER = 3.0

RADIO_IDLE = 0.5
RADIO_TX = 8.0

PAYLOAD_POWER = 5.0

# =====================================================
# ORBIT LEVEL SIMULATION
# =====================================================

orbit_minutes = np.arange(ORBIT_PERIOD_MIN)

battery = BATTERY_CAPACITY * INITIAL_SOC

orbit_soc = []
orbit_solar = []
orbit_load = []

for minute in orbit_minutes:

    # -----------------------------------
    # Solar Model
    # -----------------------------------

    if minute < SUNLIGHT_MIN:

        solar_factor = np.sin(
            np.pi * minute / SUNLIGHT_MIN
        )

        solar_power = P_SOLAR_MAX * solar_factor

    else:

        solar_power = 0

    # -----------------------------------
    # Base Load
    # -----------------------------------

    load = (
        OBC_POWER
        + ADCS_POWER
        + RADIO_IDLE
    )

    # -----------------------------------
    # Downlink Window
    # -----------------------------------

    if 20 <= minute <= 30:
        load += RADIO_TX

    # -----------------------------------
    # Imaging Window
    # -----------------------------------

    if 40 <= minute <= 45:
        load += PAYLOAD_POWER

    # -----------------------------------
    # Battery Update
    # -----------------------------------

    battery += (solar_power - load) / 60

    battery = max(
        0,
        min(BATTERY_CAPACITY, battery)
    )

    orbit_soc.append(battery)
    orbit_solar.append(solar_power)
    orbit_load.append(load)

# =====================================================
# YEAR SIMULATION
# =====================================================

battery = BATTERY_CAPACITY * INITIAL_SOC

soc_year = []

for day in range(MISSION_DAYS):

    # -----------------------------------
    # Solar degradation
    # -----------------------------------

    solar_degradation = (
        1
        - SOLAR_EOL_LOSS * (day / MISSION_DAYS)
    )

    # -----------------------------------
    # Battery degradation
    # -----------------------------------

    battery_capacity_today = (
        BATTERY_CAPACITY
        * (
            1
            - BATTERY_EOL_LOSS
            * (day / MISSION_DAYS)
        )
    )

    # -----------------------------------
    # Seasonal illumination variation
    # -----------------------------------

    seasonal_factor = (
        0.95
        + 0.05
        * np.sin(
            2 * np.pi * day / 365
        )
    )

    # -----------------------------------
    # Average daily solar energy
    # -----------------------------------

    avg_solar_power = (
        12
        * solar_degradation
        * seasonal_factor
    )

    energy_generated = (
        avg_solar_power
        * (
            SUNLIGHT_MIN / 60
        )
        * ORBITS_PER_DAY
    )

    # -----------------------------------
    # Daily load estimate
    # -----------------------------------

    avg_load = 7.5

    energy_consumed = (
        avg_load * 24
    )

    # -----------------------------------
    # Battery Update
    # -----------------------------------

    net_energy = (
        energy_generated
        - energy_consumed
    )

    battery += net_energy / 50

    battery = max(
        0,
        min(
            battery_capacity_today,
            battery
        )
    )

    soc_year.append(battery)

# =====================================================
# PLOTS
# =====================================================

# -----------------------------------
# 1 ORBIT
# -----------------------------------

plt.figure(figsize=(12,6))

plt.plot(
    orbit_minutes,
    orbit_solar,
    label="Solar Power (W)"
)

plt.plot(
    orbit_minutes,
    orbit_load,
    label="Load Power (W)"
)

plt.plot(
    orbit_minutes,
    orbit_soc,
    label="Battery SOC (Wh)"
)

plt.title("Single Orbit Analysis")

plt.xlabel("Orbit Minute")
plt.ylabel("Power / Energy")

plt.grid(True)

plt.legend()

plt.show()

# -----------------------------------
# 1 WEEK
# -----------------------------------

plt.figure(figsize=(12,6))

plt.plot(
    np.arange(7),
    soc_year[:7],
    marker="o"
)

plt.title("Battery State of Charge - First Week")

plt.xlabel("Mission Day")
plt.ylabel("Battery Energy (Wh)")

plt.grid(True)

plt.show()

# -----------------------------------
# 1 MONTH
# -----------------------------------

plt.figure(figsize=(12,6))

plt.plot(
    np.arange(30),
    soc_year[:30]
)

plt.title("Battery State of Charge - First Month")

plt.xlabel("Mission Day")
plt.ylabel("Battery Energy (Wh)")

plt.grid(True)

plt.show()

# -----------------------------------
# 1 YEAR
# -----------------------------------

plt.figure(figsize=(12,6))

plt.plot(
    np.arange(MISSION_DAYS),
    soc_year
)

plt.title("Battery State of Charge - One Year Mission")

plt.xlabel("Mission Day")
plt.ylabel("Battery Energy (Wh)")

plt.grid(True)

plt.show()

# =====================================================
# RESULTS
# =====================================================

print("\n============================")
print("MISSION RESULTS")
print("============================")

print(
    f"Initial SOC: {soc_year[0]:.2f} Wh"
)

print(
    f"Final SOC: {soc_year[-1]:.2f} Wh"
)

print(
    f"Minimum SOC: {min(soc_year):.2f} Wh"
)

if min(soc_year) > 0:
    print("✅ Mission Survives 1 Year")
else:
    print("❌ Mission Failure")

print(
    f"Solar Array Peak Power: {P_SOLAR_MAX:.2f} W"
)