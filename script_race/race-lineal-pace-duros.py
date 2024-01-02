import fastf1 as FastF1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta

FastF1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')

# Get session data
session = FastF1.get_session(2023, 'Miami', 'FP2')
session.load()
laps = session.laps

# Filter laps by track status
laps = laps[laps['TrackStatus'] == '1']

laps = laps[laps['Compound'] == 'HARD']

# Get list of drivers
drivers = ['ALO']

color = {}
linestyles = ['-', '--', '-.', ':']

# Calculate lap times for each driver
driver_lap_times = {}
for driver in drivers:
    print(driver)
    driver_laps = laps.pick_driver(driver)
    lap_times = driver_laps['LapTime'].dropna()
    team_driver = driver_laps['Team'].iloc[0]
    color_driver = FastF1.plotting.team_color(team_driver)
    lap_times_seconds = [lap_time.total_seconds() for lap_time in lap_times]
    color[driver] = color_driver
    driver_lap_times[driver] = lap_times_seconds

# Create line chart
plt.figure(figsize=(12, 6))
for i, (driver, lap_times) in enumerate(driver_lap_times.items()):
    linestyle = linestyles[i % len(linestyles)]
    plt.plot(lap_times, label=driver, color=color[driver], linestyle=linestyle)
plt.legend()
plt.xlabel('Lap Number')
plt.ylabel('Lap Time (s)')
plt.gca().set_xlim([0, max([len(lap_times) for lap_times in driver_lap_times.values()])])

plt.show()

# Write laps to text file
with open('lapsp.txt', 'w') as f:
    for index, lap in laps.iterrows():
        driver = lap['Driver']
        lap_number = lap['LapNumber']
        lap_time = lap['LapTime']
        if pd.isna(lap_time):
            continue
        total_seconds = lap_time.total_seconds()
        minutes, seconds = divmod(total_seconds, 60)
        lap_time_formatted = f'{int(minutes):02d}:{seconds:06.3f}'
        f.write(f'hola')
        f.write(f'{driver} Lap {lap_number}: {lap_time_formatted}\n')