import fastf1 as ff1
from fastf1 import plotting
from fastf1.api import track_status_data
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

ff1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')
ff1.plotting.setup_mpl()
# cargar la sesion
session = ff1.get_session(2023, 'Monaco', 'FP1')
laps = session.load_laps(with_telemetry=True)

driver_1, driver_2, driver_3 = 'ALO', 'LEC', 'VER'

# elegimos la vuelta rapida de cada piloto
laps_driver_1 = session.laps.pick_driver(driver_1)
laps_driver_2 = session.laps.pick_driver(driver_2)
laps_driver_3 = session.laps.pick_driver(driver_3)
  
fastest_driver_1 = session.laps.pick_driver(driver_1).pick_fastest()
fastest_driver_2 = session.laps.pick_driver(driver_2).pick_fastest()
fastest_driver_3 = session.laps.pick_driver(driver_3).pick_fastest()

telemetry_driver_1 = fastest_driver_1.get_telemetry()
telemetry_driver_2 = fastest_driver_2.get_telemetry()
telemetry_driver_3 = fastest_driver_3.get_telemetry()

team_driver_1 = laps_driver_1['Team'].iloc[0]
team_driver_2 = laps_driver_2['Team'].iloc[0]
team_driver_3 = laps_driver_3['Team'].iloc[0]
color_1 = ff1.plotting.team_color(team_driver_1)
color_2 = ff1.plotting.team_color(team_driver_2)
color_3 = ff1.plotting.team_color(team_driver_3)

telemetry_driver_1['Driver'] = driver_1
telemetry_driver_2['Driver'] = driver_2
telemetry_driver_3['Driver'] = driver_3

telemetry = pd.concat([telemetry_driver_1, telemetry_driver_2, telemetry_driver_3])
num_minisectors = 25
total_distance = max(telemetry['Distance'])
minisector_length = total_distance / num_minisectors

minisectors = [0]

for i in range(0, (num_minisectors - 1)):minisectors.append(minisector_length * (i + 1))

# Assign a minisector number to every row in the telemetry dataframe
telemetry['Minisector'] = telemetry['Distance'].apply(lambda dist: (int((dist // minisector_length) + 1)))
# Calculate minisector speeds per driver
average_speed = telemetry.groupby(['Minisector','Driver'])['Speed'].mean().reset_index()

# Per minisector, find the fastest driver
fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]
fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})

# Merge the fastest_driver dataframe to the telemetry dataframe on minisector
telemetry = telemetry.merge(fastest_driver, on=['Minisector'])
telemetry = telemetry.sort_values(by=['Distance'])

print(telemetry['Fastest_driver'])
total_drivers = len(telemetry['Fastest_driver'])
fastest_drivers = np.count_nonzero(telemetry['Fastest_driver'] == driver_1)
second_fastest_drivers = np.count_nonzero(telemetry['Fastest_driver'] == driver_2)
third_fastest_drivers = np.count_nonzero(telemetry['Fastest_driver'] == driver_3)

fastest_drivers_percentage = (fastest_drivers / total_drivers) * 100
second_fastest_drivers_percentage = (second_fastest_drivers / total_drivers) * 100
third_fastest_drivers_percentage = (third_fastest_drivers / total_drivers) * 100

print(f'Porcentaje de {driver_1}: {fastest_drivers_percentage}%')
print(f'Porcentaje de {driver_2}: {second_fastest_drivers_percentage}%')
print(f'Porcentaje de {driver_3}s: {third_fastest_drivers_percentage}%')

# Since our plot can only work with integers, we need to convert the driver abbreviations to integers (1 or 2)
telemetry.loc[telemetry['Fastest_driver'] == driver_1,
'Fastest_driver_int'] = 1
telemetry.loc[telemetry['Fastest_driver'] == driver_2,
'Fastest_driver_int'] = 2
telemetry.loc[telemetry['Fastest_driver'] == driver_3,
'Fastest_driver_int'] = 3
# Get the x and y coordinates
x = np.array(telemetry['X'].values)
y = np.array(telemetry['Y'].values)

# Convert the coordinates to points, and then concat them into segments
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(
float)
# The segments we just created can now be colored according to the fastest driver in a minisector
cmap = ListedColormap([color_1, color_2, color_3])
lc_comp = LineCollection(segments,
        norm=plt.Normalize(1, cmap.N + 1),
        cmap=cmap)
lc_comp.set_array(fastest_driver_array)
lc_comp.set_linewidth(6)
# Create the plot
plt.rcParams['figure.figsize'] = [18, 10]
plt.title(f'Lap Comparison between {driver_1} and {driver_2} and {driver_3}')
plt.gca().add_collection(lc_comp)
plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} VS {driver_2} VS {driver_3}"
plot_filename = plot_title.replace(" ", "") + ".png"
plt.axis('equal')
plt.tick_params(labelleft=False, left=False,
labelbottom=False, bottom=False)


# Load the image
image = plt.imread(r'C:\Users\jorge\Desktop\fastf1\script_qualy\logo-graf-blanco.png')

# Create an OffsetImage with the image and desired opacity
imagebox = OffsetImage(image, zoom=0.5, alpha=0.23)

# Get the current axes limits
xlim = plt.xlim()
ylim = plt.ylim()

# Compute the center of the y-axis
ycenter = ylim[0] / 2

# Compute half of the maximum x-value
xcenter = xlim[1] / 2

# Create an AnnotationBbox with the OffsetImage and desired position
ab = AnnotationBbox(imagebox, (xcenter, ycenter), frameon=False)

# Add the AnnotationBbox to the current axes
plt.gca().add_artist(ab)
plt.savefig("lapcomparison.png")
plt.savefig(plot_filename, dpi=300)
plt.show()
