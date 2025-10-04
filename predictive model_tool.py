def plot_battery_temperature_comparison(params):
    """
    Simulates and plots battery discharge/charge cycles and corresponding 
    temperature changes during a workday with a lunch break.
    
    Parameters
    ----------
    params : dict
        Dictionary containing simulation parameters:
        - initial_battery_percentage (float): starting battery percentage (0–100).
        - initial_temperature (float): starting device temperature (°C).
        - mean_tau_discharging (float): time constant for exponential battery discharge.
        - mean_tau_charging (float): time constant for exponential battery charging.
        - mean_tau_temp_discharge (float): time constant for temperature increase during discharge.
        - mean_tau_temp_charge (float): time constant for cooling/heating during charging.
        - discharge_time (int): discharge period per cycle (minutes).
        - charge_time (int): charge period per cycle (minutes).
        - temp_threshold (float): max allowable temperature (°C).
    """

    # ---------------- Battery + Temperature Models ---------------- #

    def discharging_model_battery(t, V0, tau, V_final=6):
        """
        Exponential discharge model for battery percentage.
        Approaches V_final asymptotically.
        """
        return V_final + (V0 - V_final) * np.exp(-t / tau)

    def charging_model_battery(t, V0, tau, V_final=100):
        """
        Exponential charging model for battery percentage.
        Saturates at V_final (default 100%).
        """
        return V_final - (V_final - V0) * np.exp(-t / tau)

    def discharging_model_temp(t, T0, tau, delta_T=10, threshold=45):
        """
        Temperature rise model during discharge.
        - Increases exponentially by delta_T.
        - Hard capped at 'threshold' (simulates thermal throttling).
        """
        temp = T0 + delta_T * (1 - np.exp(-t / tau))
        temp_capped = np.minimum(temp, threshold)

        # Apply threshold: once reached, temperature is fixed at cap.
        for i in range(1, len(temp_capped)):
            if temp_capped[i] == threshold:
                temp_capped[i:] = threshold
                break
        return temp_capped

    def charging_model_temp(t, T0, tau, T_final):
        """
        Temperature relaxation during charging.
        Decays exponentially toward T_final (baseline temperature).
        """
        return T_final + (T0 - T_final) * np.exp(-t / tau)

    # ---------------- Workday Simulation ---------------- #

    def simulate_workday_with_break(discharge_time, charge_time, initial_battery_percentage, initial_temperature,
                                    tau_discharging, tau_charging, tau_temp_discharge, tau_temp_charge, temp_threshold):
        """
        Simulates a full workday:
        - Work session → battery discharges, temperature rises.
        - Charging session → battery charges, temperature relaxes.
        - Midday 1-hour break → battery charges continuously.
        """
        # Define time anchors
        workday_start_time = datetime(2024, 10, 12, 8, 0)
        break_start_time   = datetime(2024, 10, 12, 12, 0)
        break_end_time     = datetime(2024, 10, 12, 13, 0)
        workday_end_time   = datetime(2024, 10, 12, 16, 0)

        battery_percentage, temperature, time = [], [], []
        current_time = workday_start_time

        # Initialize state
        battery = initial_battery_percentage
        temp = initial_temperature

        # Loop through timeline until end of day
        while current_time < workday_end_time:
            # Case 1: Lunch break (continuous charging)
            if break_start_time <= current_time < break_end_time:
                break_time_points = np.arange(0, 60, 1)  # 60 min resolution
                charge_during_break = np.minimum(
                    charging_model_battery(break_time_points, battery, tau_charging), 100
                )
                temp_during_break = charging_model_temp(
                    break_time_points, temp, tau_temp_charge, T_final=params["initial_temperature"]
                )

                # Update histories
                battery_percentage.extend(charge_during_break)
                temperature.extend(temp_during_break)
                time.extend([current_time + timedelta(minutes=i) for i in range(len(break_time_points))])

                # Update state
                battery, temp = charge_during_break[-1], temp_during_break[-1]
                current_time += timedelta(minutes=len(break_time_points))

            # Case 2: Regular work cycle (discharge + recharge)
            else:
                # Discharge phase
                discharge_time_points = np.arange(0, discharge_time, 1)
                discharge_temp = discharging_model_temp(
                    discharge_time_points, temp, tau_temp_discharge, threshold=temp_threshold
                )
                discharge_battery = discharging_model_battery(discharge_time_points, battery, tau_discharging)

                battery_percentage.extend(discharge_battery)
                temperature.extend(discharge_temp)
                time.extend([current_time + timedelta(minutes=i) for i in range(len(discharge_time_points))])
                battery, temp = discharge_battery[-1], discharge_temp[-1]
                current_time += timedelta(minutes=len(discharge_time_points))

                # Charge phase
                charge_time_points = np.arange(0, charge_time, 1)
                charge_temp = charging_model_temp(
                    charge_time_points, temp, tau_temp_charge, T_final=params["initial_temperature"]
                )
                charge_battery = np.minimum(
                    charging_model_battery(charge_time_points, battery, tau_charging), 100
                )

                battery_percentage.extend(charge_battery)
                temperature.extend(charge_temp)
                time.extend([current_time + timedelta(minutes=i) for i in range(len(charge_time_points))])
                battery, temp = charge_battery[-1], charge_temp[-1]
                current_time += timedelta(minutes=len(charge_time_points))

        return time, battery_percentage, temperature

    # ---------------- Extract Parameters ---------------- #

    initial_battery_percentage = params["initial_battery_percentage"]
    initial_temperature        = params["initial_temperature"]
    mean_tau_discharging       = params["mean_tau_discharging"]
    mean_tau_charging          = params["mean_tau_charging"]
    mean_tau_temp_discharge    = params["mean_tau_temp_discharge"]
    mean_tau_temp_charge       = params["mean_tau_temp_charge"]
    discharge_time             = params["discharge_time"]
    charge_time                = params["charge_time"]
    temp_threshold             = params["temp_threshold"]

    # ---------------- Run Simulation ---------------- #

    time, battery, temperature = simulate_workday_with_break(
        discharge_time, charge_time, initial_battery_percentage,
        initial_temperature, mean_tau_discharging, mean_tau_charging,
        mean_tau_temp_discharge, mean_tau_temp_charge, temp_threshold
    )

    # ---------------- Plot Results ---------------- #

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Battery % on primary y-axis
    ax1.plot(time, battery, label="Battery Percentage (%)", color="teal")
    ax1.axvline(x=datetime(2024, 10, 12, 12, 0), color='blue', linestyle='--', label="1-Hour Break (12 PM)")
    ax1.set_xlabel("Time (hours)")
    ax1.set_ylabel("Battery Percentage (%)", color="teal")
    ax1.tick_params(axis='y', labelcolor="teal")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))  # integer ticks

    # Temperature on secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(time, temperature, label="Temperature (°C)", color='orange', linestyle='--')
    ax2.set_ylabel("Temperature (°C)", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    ax2.axhline(y=temp_threshold, color='red', linestyle='--', label=f"Temperature Threshold ({temp_threshold}°C)")

    # Time axis formatting
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    ax1.xaxis.set_major_locator(mdates.HourLocator())

    # Layout + legends
    fig.tight_layout()
    ax1.legend(loc="upper left", bbox_to_anchor=(0, 1.15))
    ax2.legend(loc="upper right", bbox_to_anchor=(1, 1.15))
    plt.grid()
    plt.show()

    plot_battery_temperature_comparison(simulation_params)
