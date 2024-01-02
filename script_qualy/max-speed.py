import fastf1 as ff1
from fastf1 import plotting
from fastf1.api import track_status_data
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection

#funcionaaaa, vuelta rapida

ff1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')  # habilitar el caché para acelerar la carga de datos
session = ff1.get_session(2023, 'Monaco', 'FP1')  # obtener la sesión de clasificación del GP de Bahrein 2022
laps = session.load_laps(with_telemetry=True)  # cargar las vueltas con telemetría

drivers = session.drivers  # obtener la lista de pilotos
max_speeds = []  # lista para almacenar la velocidad máxima de cada piloto
driver_code = []
color_driver = []

for driver in drivers:
    color_driver.append(ff1.plotting.team_color(laps.pick_driver(driver)['Team'].iloc[0]))
    name_driver = laps.pick_driver(driver).iloc[0]['Driver']
    driver_laps = laps.pick_driver(driver).pick_fastest().get_telemetry() # obtener las vueltas del piloto
    max_speed = max(driver_laps['Speed'])  # calcular la velocidad máxima
    max_speeds.append(max_speed)
    driver_code.append(name_driver)

# ordenar las listas max_speeds y driver_code en orden descendente
sort_idx = np.argsort(max_speeds)[::-1]
color_driver = [color_driver[i] for i in sort_idx]
max_speeds = [max_speeds[i] for i in sort_idx]
driver_code = [driver_code[i] for i in sort_idx]

x_pos = range(len(drivers))  # posiciones en el eje x para las barras
plt.bar(x_pos, max_speeds, color=color_driver)  # crear un gráfico de barras con las velocidades máximas y asignar un color a cada barra

# agregar etiquetas encima de cada barra
for i in range(len(max_speeds)):
    plt.text(x=x_pos[i], y=max_speeds[i]+1, s=f"{driver_code[i]}\n{max_speeds[i]:.0f}", ha='center')

plt.xlabel('Piloto')
plt.ylabel('Velocidad máxima (km/h)')
plt.show()