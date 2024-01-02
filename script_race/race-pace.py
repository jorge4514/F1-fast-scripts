import fastf1 as ff1
from matplotlib import pyplot as plt

# Set up FastF1
ff1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')
# Get the race data
race = ff1.get_session(2023, 'Monaco', 'R')
laps = race.load_laps(with_telemetry=False)

# Get the track status data
track_status = ff1.api.track_status_data(race)

# Filter out laps that were not under green flag conditions
green_flag_laps = laps[laps['LapStartTime'].apply(lambda x: track_status.at_time(x).iloc[0]['Status']) == 'TrackClear']

# Calculate the average lap time for each driver
driver_avg_lap_times = green_flag_laps.groupby('Driver')['LapTime'].mean()

# Find the fastest driver
fastest_driver = driver_avg_lap_times.idxmin()
fastest_driver_avg_lap_time = driver_avg_lap_times[fastest_driver]

# Calculate the difference in average lap time between the fastest driver and the rest of the drivers
lap_time_diff = driver_avg_lap_times - fastest_driver_avg_lap_time

# Convert the Timedelta objects to seconds
lap_time_diff_seconds = lap_time_diff.dt.total_seconds()

# Sort the lap time differences in ascending order
lap_time_diff_seconds_sorted = lap_time_diff_seconds.sort_values()

# Plot the lap time differences
ax = lap_time_diff_seconds_sorted.plot(kind='bar')

# Add the lap time differences as labels to the bar chart
for i, v in enumerate(lap_time_diff_seconds_sorted):
    ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')

plt.show()