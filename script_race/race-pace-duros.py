import fastf1 as FastF1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta

FastF1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')

# Get session data
session = FastF1.get_session(2023, 'Monaco', 'R')
session.load()
laps = session.laps

# Filter laps by track status
laps = laps[laps['TrackStatus'] == '1']

laps = laps[laps['Compound'] == 'HARD']

# Get list of drivers
drivers = laps['Driver'].unique()
color = {}

# Calculate average lap time for each driver
avg_lap_times = {}
for driver in drivers:
    driver_laps = laps.pick_driver(driver)
    lap_times = driver_laps['LapTime'].dropna()
    team_driver = driver_laps['Team'].iloc[0]
    color_driver = FastF1.plotting.team_color(team_driver)
    avg_lap_time = lap_times.mean()
    color[driver] = color_driver
    avg_lap_times[driver] = avg_lap_time

# Sort drivers by average lap time
sorted_drivers = sorted(avg_lap_times, key=avg_lap_times.get)

# Calculate difference from first driver
first_driver_avg_lap_time = avg_lap_times[sorted_drivers[0]]
differences = {}
for driver in sorted_drivers:
    difference = avg_lap_times[driver] - first_driver_avg_lap_time
    differences[driver] = difference

# Sort drivers by difference from first driver
sorted_drivers = sorted(differences, key=differences.get)

# Create bar chart
x = range(len(sorted_drivers))
y = [differences[driver].total_seconds() for driver in sorted_drivers]
bars = plt.bar(x, y, color=[color[driver] for driver in sorted_drivers])
plt.xticks(x, sorted_drivers, rotation=90)
plt.ylabel('Difference from First Driver (s)')

# Add labels to bars
for bar in bars:
    height = bar.get_height()
    label_x_pos = bar.get_x() + bar.get_width() / 2
    label_y_pos = height + 0.05
    plt.text(label_x_pos, label_y_pos, f'{height:.3f}', ha='center', va='bottom')

plt.show()

# Write laps to text file
with open('laps.txt', 'w') as f:
    for index, lap in laps.iterrows():
        driver = lap['Driver']
        lap_number = lap['LapNumber']
        lap_time = lap['LapTime']
        if pd.isna(lap_time):
            continue
        total_seconds = lap_time.total_seconds()
        minutes, seconds = divmod(total_seconds, 60)
        lap_time_formatted = f'{int(minutes):02d}:{seconds:06.3f}'
        f.write(f'{driver} Lap {lap_number}: {lap_time_formatted}\n')