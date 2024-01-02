import fastf1 as FastF1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta

FastF1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')

# Get session data
session = FastF1.get_session(2023, 'Baku', 'S')
session.load()
laps = session.laps

# Filter laps by driver
driver_laps = laps.pick_driver('RUS')

with open('lap_times.txt', 'w') as f:
    for index, lap in driver_laps.iterrows():
        lap_number = lap['LapNumber']
        lap_time = lap['LapTime']
        if pd.isna(lap_time):
            continue
        total_seconds = lap_time.total_seconds()
        minutes, seconds = divmod(total_seconds, 60)
        lap_time_formatted = f'{int(minutes):02d}:{seconds:06.3f}'
        f.write(f'Lap {lap_number}: {lap_time_formatted}\n')