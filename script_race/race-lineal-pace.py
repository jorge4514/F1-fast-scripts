import fastf1 as FastF1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

FastF1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')

# Get session data
session = FastF1.get_session(2023, 'Miami', 'R')
session.load()
laps = session.laps

# Filter laps by track status
laps = laps[(laps['TrackStatus'] == '1') & (laps['IsAccurate'] == True)]

# Get list of drivers
drivers = laps['Driver'].unique()[:10]

color = {}
linestyles = ['dashed', 'dashed', 'dashed', 'dashed']

# Create the plot
# Set the DPI to 100 so that 1 inch = 100 pixels
DPI = 100

# Set the figure size in inches
fig = plt.figure(figsize=(1000/DPI, 1000/DPI), dpi=DPI)

# Calculate lap times for each driver
driver_lap_times = {}
for driver in drivers:
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
# Load the image
image = plt.imread(r'C:\Users\jorge\Desktop\fastf1\script_qualy\logo-graf.png')

# Create an OffsetImage with the image and desired opacity
imagebox = OffsetImage(image, zoom=0.5, alpha=0.23)

# Get the current axes limits
xlim = plt.xlim()
ylim = plt.ylim()

# Compute the center of the y-axis
ycenter = ylim[0] + ylim[1] / 2

# Compute half of the maximum x-value
xcenter = xlim[1] / 2

# Create an AnnotationBbox with the OffsetImage and desired position
ab = AnnotationBbox(imagebox, (xcenter, ycenter), frameon=False)
# Add the AnnotationBbox to the current axes
plt.gca().add_artist(ab)
plt.legend()
plt.xlabel('Lap Number')
plt.ylabel('Lap Time (s)')
plt.ylim(90, 95)
plt.gca().set_xlim([0, max([len(lap_times) for lap_times in driver_lap_times.values()])])
plt.savefig('plot.png', dpi=DPI)
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