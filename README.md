# 3U CubeSat Power System Modeling & Mission Feasibility Analysis

## Overview

This project evaluates the electrical power system performance of a 3U CubeSat operating in Low Earth Orbit (LEO). The objective is to determine whether the spacecraft remains power-positive throughout a one-year mission while accounting for solar array degradation, battery aging, orbital eclipse periods, and varying operational modes.

The model simulates energy generation, energy consumption, battery state-of-charge, and long-term system viability.

---

## Mission Description

### Mission Type

Earth Observation and Telemetry Demonstration

### Spacecraft Class

3U CubeSat

### Mission Duration

1 Year

### Orbit

| Parameter      | Value                       |
| -------------- | --------------------------- |
| Altitude       | 500 km                      |
| Orbit Type     | Sun Synchronous Orbit (SSO) |
| Orbit Period   | ~95 minutes                 |
| Orbits Per Day | ~15                         |
| Sunlight Time  | ~60 min/orbit               |
| Eclipse Time   | ~35 min/orbit               |

---

# System Architecture

## Electrical Power System (EPS)

The EPS consists of:

- Body-mounted solar arrays
- Battery energy storage
- Power regulation and distribution electronics
- Electrical load monitoring

---

## Solar Array

### Configuration

Body-mounted Triple Junction Gallium Arsenide (GaAs) cells

### Representative Vendor

EnduroSat Solar Panels

### Parameters

| Parameter                | Value     |
| ------------------------ | --------- |
| Solar Flux               | 1361 W/m² |
| Panel Area               | 0.06 m²   |
| Cell Efficiency          | 28%       |
| EPS Efficiency           | 90%       |
| Beginning-of-Life Output | ~20.6 W   |
| End-of-Life Degradation  | 20%       |

### Modeling Assumptions

- Cosine incidence losses
- Seasonal illumination variation
- Orbital eclipse periods
- 20% degradation over mission life

---

## Battery System

### Representative Vendor

GomSpace NanoPower BPX

### Configuration

Lithium-Ion Battery Pack

### Parameters

| Parameter                 | Value |
| ------------------------- | ----- |
| Capacity                  | 22 Wh |
| Initial SOC               | 80%   |
| Battery Efficiency        | 92%   |
| End-of-Life Capacity Loss | 15%   |

### Purpose

The battery must:

- Support eclipse operations
- Support high-power communication windows
- Maintain reserve capacity throughout mission life

---

## Flight Computer (OBC)

### Representative Hardware

GomSpace NanoMind A3200

### Typical Power

| Mode    | Power |
| ------- | ----- |
| Nominal | 1.5 W |

### Functions

- Command and Data Handling
- Telemetry Processing
- Mission Sequencing
- Health Monitoring

---

## Communications System

### Representative Hardware

ISISPACE TRXVU

### Power Consumption

| Mode     | Power |
| -------- | ----- |
| Receive  | 1 W   |
| Transmit | 8 W   |

### Average Orbit Power

2 W

### Functions

- Ground Station Communications
- Telemetry Downlink
- Command Uplink

---

## Attitude Determination and Control System (ADCS)

### Representative Hardware

Blue Canyon Technologies XACT

### Power Consumption

| Mode    | Power |
| ------- | ----- |
| Nominal | 3 W   |
| Peak    | 6 W   |

### Functions

- Attitude Control
- Pointing Accuracy
- Solar Tracking
- Payload Targeting

---

## Payload

### Representative Payload

Earth Observation Camera

### Power Consumption

| Mode           | Power |
| -------------- | ----- |
| Idle           | 0 W   |
| Active Imaging | 5 W   |

### Mission Function

- Earth Imaging
- Educational Demonstration
- Image Downlink

---

# Spacecraft Power Budget

| Subsystem       | Average Power |
| --------------- | ------------- |
| OBC             | 1.5 W         |
| ADCS            | 3.0 W         |
| Communications  | 2.0 W         |
| Payload Average | 0.5 W         |
| EPS Losses      | 0.5 W         |

### Total Average Load

7.5 W

---

# Operational Modes

## Safe Mode

Used during anomalies or low battery conditions.

| Parameter | Value |
| --------- | ----- |
| Load      | 4 W   |

---

## Nominal Mode

Standard spacecraft operation.

| Parameter | Value |
| --------- | ----- |
| Load      | 7.5 W |

---

## Imaging Mode

Camera acquisition operations.

| Parameter | Value |
| --------- | ----- |
| Load      | 12 W  |

---

## Downlink Mode

High-rate communications with ground stations.

| Parameter | Value |
| --------- | ----- |
| Load      | 15 W  |

---

# Power Modeling Objectives

The simulation evaluates:

- Solar power generation
- Eclipse energy deficits
- Battery state-of-charge trends
- End-of-life performance
- System energy margins
- Long-term mission survivability

---

# Key Engineering Questions

1. Does the spacecraft remain power-positive for one year?

2. What battery reserve remains at end-of-life?

3. What is the minimum solar array area required?

4. How sensitive is the design to solar degradation?

5. How sensitive is the design to battery aging?

6. Can the spacecraft survive worst-case communication and imaging schedules?

---

# Future Enhancements

- High-fidelity orbital mechanics
- STK integration
- Monte Carlo analysis
- Thermal impacts on battery efficiency
- Radiation-induced solar degradation
- Power mode optimization
- Requirements verification framework

---

# Author

USF Picosatellite Organization

Solar Power Lead

Developed electrical power budgets, solar array sizing analyses, battery sizing studies, and mission energy balance simulations to verify power-positive operation throughout mission life.
