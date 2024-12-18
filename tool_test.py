import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def plot_battery_temperature_comparison(params):

    def discharging_model_battery(t, V0, tau, V_final=6):
        return V_final + (V0 - V_final) * np.exp(-t / tau)

    def charging_model_battery(t, V0, tau, V_final=100):
        return V_final - (V_final - V0) * np.exp(-t / tau)

    def discharging_model_temp(t, T0, tau, delta_T=10, threshold=40):
        temp = T0 + delta_T * (1 - np.exp(-t / tau))  
        temp_capped = np.minimum(temp, threshold)  
        for i in range(1, len(temp_capped)):
            if temp_capped[i] == threshold:
                temp_capped[i:] = threshold  
                break
        return temp_capped

    def charging_model_temp(t, T0, tau, T_final):
        temp = T_final + (T0 - T_final) * np.exp(-t / tau)
        return temp

    def simulate_workday_with_break(discharge_time, charge_time, initial_battery_percentage, initial_temperature,
                                    tau_discharging, tau_charging, tau_temp_discharge, tau_temp_charge, temp_threshold):
        workday_start_time = datetime(2024, 10, 12, 8, 0)
        break_start_time = datetime(2024, 10, 12, 12, 0)
        break_end_time = datetime(2024, 10, 12, 13, 0)
        workday_end_time = datetime(2024, 10, 12, 16, 0)

        battery_percentage = [initial_battery_percentage]
        temperature = [initial_temperature]
        time = [workday_start_time]
        current_time = workday_start_time

        while current_time < workday_end_time:
            if break_start_time <= current_time < break_end_time:
                break_time_points = np.arange(0, 60, 1)
                charge_during_break = charging_model_battery(break_time_points, battery_percentage[-1], tau_charging)
                temp_during_break = charging_model_temp(
                    break_time_points, temperature[-1], tau_temp_charge, T_final=params["initial_temperature"]
                )

                battery_percentage.extend(charge_during_break)
                temperature.extend(temp_during_break)
                current_time += timedelta(minutes=60)
                time.extend([current_time - timedelta(minutes=i) for i in range(len(break_time_points), 0, -1)])
            else:
                discharge_time_points = np.arange(0, discharge_time, 1)
                discharge_temp = discharging_model_temp(
                    discharge_time_points, temperature[-1], tau_temp_discharge, threshold=temp_threshold
                )
                discharge_battery = discharging_model_battery(discharge_time_points, battery_percentage[-1], tau_discharging)

                battery_percentage.extend(discharge_battery)
                temperature.extend(discharge_temp)
                current_time += timedelta(minutes=discharge_time)
                time.extend([current_time - timedelta(minutes=i) for i in range(len(discharge_time_points), 0, -1)])

                charge_time_points = np.arange(0, charge_time, 1)
                charge_temp = charging_model_temp(
                    charge_time_points, discharge_temp[-1], tau_temp_charge, T_final=params["initial_temperature"]
                )
                charge_battery = charging_model_battery(charge_time_points, discharge_battery[-1], tau_charging)

                battery_percentage.extend(charge_battery)
                temperature.extend(charge_temp)
                current_time += timedelta(minutes=charge_time)
                time.extend([current_time - timedelta(minutes=i) for i in range(len(charge_time_points), 0, -1)])

        return time, battery_percentage, temperature

    initial_battery_percentage = params["initial_battery_percentage"]
    initial_temperature = params["initial_temperature"]
    mean_tau_discharging = params["mean_tau_discharging"]
    mean_tau_charging = params["mean_tau_charging"]
    mean_tau_temp_discharge = params["mean_tau_temp_discharge"]
    mean_tau_temp_charge = params["mean_tau_temp_charge"]
    discharge_time = params["discharge_time"]
    charge_time = params["charge_time"]
    temp_threshold = params["temp_threshold"]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    time, battery, temperature = simulate_workday_with_break(
        discharge_time, charge_time, initial_battery_percentage,
        initial_temperature, mean_tau_discharging, mean_tau_charging,
        mean_tau_temp_discharge, mean_tau_temp_charge, temp_threshold
    )

    ax1.plot(time, battery, label="Battery Percentage (%)", color="teal")
    ax1.axvline(x=datetime(2024, 10, 12, 12, 0), color='blue', linestyle='--', label="1-Hour Break (12 PM)")
    ax1.set_xlabel("Time (hours)")
    ax1.set_ylabel("Battery Percentage (%)", color="teal")
    ax1.tick_params(axis='y', labelcolor="teal")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))

    ax2 = ax1.twinx()
    ax2.plot(time, temperature, label="Temperature (°C)", color='orange', linestyle='--')
    ax2.set_ylabel("Temperature (°C)", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.axhline(y=temp_threshold, color='red', linestyle='--', label="Temperature Threshold (40°C)")

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    ax1.xaxis.set_major_locator(mdates.HourLocator())

    fig.tight_layout()
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.grid()
    plt.show()

simulation_params = {
    "initial_battery_percentage": 100,
    "initial_temperature": 32, 
    "mean_tau_discharging": 83,
    "mean_tau_charging": 9,
    "mean_tau_temp_discharge": 40,
    "mean_tau_temp_charge": 15,
    "discharge_time": 10,  
    "charge_time": 10,    
    "temp_threshold": 40  
}
plot_battery_temperature_comparison(simulation_params)
