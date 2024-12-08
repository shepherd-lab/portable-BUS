!pip install ipywidgets

import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Define discharging and charging models for battery using time constants
def discharging_model_battery(t, V0, tau, V_final=0):
    return V_final + (V0 - V_final) * np.exp(-t / tau)

def charging_model_battery(t, V0, tau, V_final=100):
    return V_final - (V_final - V0) * np.exp(-t / tau)

# Define discharging and charging models for temperature using time constants
def discharging_model_temp(t, T0, tau, T_infinity=45):
    return T_infinity - (T_infinity - T0) * np.exp(-t / tau)

def charging_model_temp(t, T0, tau, T_final=26):
    return T_final + (T0 - T_final) * np.exp(-t / tau)

# Simulate workday with specified intervals
def simulate_workday(discharge_time, charge_time, initial_battery_percentage, initial_temperature, tau_discharging, tau_charging, tau_temp_discharge, tau_temp_charge):
    workday_start_time = datetime(2024, 1, 1, 8, 0)  # Start at 8:00 AM
    workday_end_time = datetime(2024, 1, 1, 16, 0)  # End at 4:00 PM

    battery_percentage = [initial_battery_percentage]
    temperature = [initial_temperature]
    time = [workday_start_time]
    current_time = workday_start_time

    while current_time < workday_end_time:
        # Discharging phase
        discharge_time_points = np.arange(0, discharge_time, 1)
        discharge_battery = discharging_model_battery(discharge_time_points, battery_percentage[-1], tau_discharging)
        discharge_temp = discharging_model_temp(discharge_time_points, temperature[-1], tau_temp_discharge)
        battery_percentage.extend(discharge_battery)
        temperature.extend(discharge_temp)
        current_time += timedelta(minutes=discharge_time)
        time.extend([current_time - timedelta(minutes=i) for i in range(len(discharge_time_points), 0, -1)])

        # Charging phase
        charge_time_points = np.arange(0, charge_time, 1)
        charge_battery = charging_model_battery(charge_time_points, discharge_battery[-1], tau_charging)
        charge_temp = charging_model_temp(charge_time_points, discharge_temp[-1], tau_temp_charge)
        battery_percentage.extend(charge_battery)
        temperature.extend(charge_temp)
        current_time += timedelta(minutes=charge_time)
        time.extend([current_time - timedelta(minutes=i) for i in range(len(charge_time_points), 0, -1)])

    return time, battery_percentage, temperature

# Example usage
initial_battery_percentage = 100
initial_temperature = 26
mean_tau_discharging = 83
mean_tau_charging = 9
mean_tau_temp_discharge = 40
mean_tau_temp_charge = 15

# Change discharge and charge timing interval
time, battery, temp = simulate_workday(
    discharge_time=3,
    charge_time=2,
    initial_battery_percentage=initial_battery_percentage,
    initial_temperature=initial_temperature,
    tau_discharging=mean_tau_discharging,
    tau_charging=mean_tau_charging,
    tau_temp_discharge=mean_tau_temp_discharge,
    tau_temp_charge=mean_tau_temp_charge
)

# Plotting results
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot battery percentage on the left y-axis
ax1.plot(time, battery, label="Battery Percentage (%)", color="teal")
ax1.set_xlabel("Time (hours)", fontsize=12)
ax1.set_ylabel("Battery Percentage (%)", color="teal", fontsize=12)
ax1.tick_params(axis='y', labelcolor="teal", labelsize=10)


# Create a second y-axis for temperature
ax2 = ax1.twinx()
ax2.plot(time, temp, label="Temperature (°C)", color="orange", linestyle="--")
ax2.set_ylabel("Temperature (°C)", color="orange", fontsize=12)
ax2.tick_params(axis='y', labelcolor="orange", labelsize=10)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))

# Add a horizontal line for the overheating threshold
ax2.axhline(y=45, color='orange', linestyle='--', label="Overheating Threshold (45°C)")

# Format x-axis to show time
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
ax1.xaxis.set_major_locator(mdates.HourLocator())

# Formatting and legend
plt.title("Workday Simulation: Battery Percentage and Temperature", fontsize=14)
fig.tight_layout()
ax1.legend(loc="upper left", fontsize=8, framealpha=0.8)
ax2.legend(loc="upper right", fontsize=8, framealpha=0.8)
plt.grid()
plt.show()
