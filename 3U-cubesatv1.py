import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# CUBESAT POWER SYSTEM MODEL
# =====================================================

# -----------------------------------------------------
# MISSION PARAMETERS
# -----------------------------------------------------

MISSION_DAYS = 365

ORBIT_PERIOD_MIN = 95
SUNLIGHT_MIN = 60
ECLIPSE_MIN = 35
ORBITS_PER_DAY = 15

# -----------------------------------------------------
# SOLAR ARRAY
# -----------------------------------------------------

SOLAR_FLUX = 1361          # W/m²

SOLAR_AREA = 0.06          # m²

CELL_EFFICIENCY = 0.28

SYSTEM_EFFICIENCY = 0.90

SOLAR_EOL_LOSS = 0.20      # 20% degradation over mission

P_SOLAR_MAX = (
    SOLAR_FLUX
    * SOLAR_AREA
    * CELL_EFFICIENCY
    * SYSTEM_EFFICIENCY
)

# -----------------------------------------------------
# BATTERY
# -----------------------------------------------------

BATTERY_CAPACITY = 22.0    # Wh

BATTERY_EOL_LOSS = 0.15

INITIAL_SOC_PERCENT = 80

# -----------------------------------------------------
# SUBSYSTEMS
# -----------------------------------------------------

# GomSpace NanoMind OBC
OBC_POWER = 1.5

# Blue Canyon XACT ADCS
ADCS_POWER = 3.0

# ISISPACE TRXVU Radio
RADIO_IDLE = 0.5
RADIO_TX = 8.0

# Imaging Payload
PAYLOAD_POWER = 5.0

# =====================================================
# ORBIT SIMULATION
# =====================================================

battery_wh = (
    BATTERY_CAPACITY
    * INITIAL_SOC_PERCENT
    / 100
)

orbit_minutes = np.arange(ORBIT_PERIOD_MIN)

orbit_soc = []
orbit_solar = []
orbit_load = []

for minute in orbit_minutes:

    # -------------------------------
    # SOLAR GENERATION
    # -------------------------------

    if minute < SUNLIGHT_MIN:

        sun_factor = np.sin(
            np.pi * minute / SUNLIGHT_MIN
        )

        solar_power = (
            P_SOLAR_MAX
            * sun_factor
        )

    else:

        solar_power = 0

    # -------------------------------
    # LOADS
    # -------------------------------

    load_power = (
        OBC_POWER
        + ADCS_POWER
        + RADIO_IDLE
    )

    # Downlink Pass

    if 20 <= minute <= 30:
        load_power += RADIO_TX

    # Imaging Pass

    if 40 <= minute <= 45:
        load_power += PAYLOAD_POWER

    # -------------------------------
    # BATTERY UPDATE
    # -------------------------------

    battery_wh += (
        solar_power
        - load_power
    ) / 60

    battery_wh = max(
        0,
        min(
            BATTERY_CAPACITY,
            battery_wh
        )
    )

    soc_percent = (
        battery_wh
        / BATTERY_CAPACITY
        * 100
    )

    orbit_soc.append(soc_percent)
    orbit_solar.append(solar_power)
    orbit_load.append(load_power)

# =====================================================
# YEAR SIMULATION
# =====================================================

battery_wh = (
    BATTERY_CAPACITY
    * INITIAL_SOC_PERCENT
    / 100
)

soc_year = []

mission_failed = False
failure_day = None

for day in range(MISSION_DAYS):

    # Solar degradation

    solar_degradation = (
        1
        - SOLAR_EOL_LOSS
        * (day / MISSION_DAYS)
    )

    # Battery degradation

    battery_capacity_today = (
        BATTERY_CAPACITY
        * (
            1
            - BATTERY_EOL_LOSS
            * (day / MISSION_DAYS)
        )
    )

    # Seasonal variation

    seasonal_factor = (
        0.95
        + 0.05
        * np.sin(
            2
            * np.pi
            * day
            / 365
        )
    )

    avg_solar_power = (
        12
        * solar_degradation
        * seasonal_factor
    )

    energy_generated = (
        avg_solar_power
        * (SUNLIGHT_MIN / 60)
        * ORBITS_PER_DAY
    )

    avg_load = 7.5

    energy_consumed = (
        avg_load
        * 24
    )

    net_energy = (
        energy_generated
        - energy_consumed
    )

    battery_wh += net_energy / 50

    if (
        battery_wh <= 0
        and not mission_failed
    ):
        mission_failed = True
        failure_day = day

    battery_wh = max(
        0,
        min(
            battery_capacity_today,
            battery_wh
        )
    )

    soc_percent = (
        battery_wh
        / battery_capacity_today
        * 100
    )

    soc_year.append(soc_percent)

# =====================================================
# RESULTS
# =====================================================

print("\n================================")
print("CUBESAT MISSION RESULTS")
print("================================")

print(
    f"Solar Array Peak Power: {P_SOLAR_MAX:.2f} W"
)

print(
    f"Initial SOC: {soc_year[0]:.1f}%"
)

print(
    f"Final SOC: {soc_year[-1]:.1f}%"
)

print(
    f"Minimum SOC: {min(soc_year):.1f}%"
)

if mission_failed:

    mission_percent = (
        failure_day
        / MISSION_DAYS
        * 100
    )

    print(
        f"\n❌ Mission Failed on Day {failure_day}"
    )

    print(
        f"Mission Life Achieved: "
        f"{mission_percent:.1f}%"
    )

else:

    print(
        "\n✅ Mission Survived Full Year"
    )

# =====================================================
# PLOT 1
# SINGLE ORBIT
# =====================================================

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
    label="Battery SOC (%)"
)

plt.title(
    "Single Orbit Power Analysis"
)

plt.xlabel(
    "Orbit Minute"
)

plt.ylabel(
    "Power / SOC"
)

plt.grid(True)

plt.legend()

plt.show()

# =====================================================
# PLOT 2
# FIRST WEEK
# =====================================================

plt.figure(figsize=(12,6))

plt.plot(
    np.arange(1,8),
    soc_year[:7],
    marker="o"
)

plt.title(
    "Battery State of Charge - First Week"
)

plt.xlabel(
    "Mission Day"
)

plt.ylabel(
    "SOC (%)"
)

plt.ylim(0,100)

plt.grid(True)

plt.show()

# =====================================================
# PLOT 3
# FIRST MONTH
# =====================================================

plt.figure(figsize=(12,6))

plt.plot(
    np.arange(1,31),
    soc_year[:30]
)

plt.title(
    "Battery State of Charge - First Month"
)

plt.xlabel(
    "Mission Day"
)

plt.ylabel(
    "SOC (%)"
)

plt.ylim(0,100)

plt.grid(True)

plt.show()

# =====================================================
# PLOT 4
# FULL YEAR
# =====================================================

plt.figure(figsize=(12,6))

plt.plot(
    np.arange(MISSION_DAYS),
    soc_year
)

plt.title(
    "Battery State of Charge - Full Year"
)

plt.xlabel(
    "Mission Day"
)

plt.ylabel(
    "SOC (%)"
)

plt.ylim(0,100)

plt.grid(True)

plt.show()