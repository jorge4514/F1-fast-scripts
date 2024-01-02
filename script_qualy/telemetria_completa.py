import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import fastf1.plotting
from fastf1 import utils

fastf1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache')

#cargar la sesion
session = fastf1.get_session(2023, 'Monaco', 'Q')
laps = session.load_laps(with_telemetry=True)

driver_1, driver_2 = 'VER', 'ALO'

#elegimos la vuelta rapida de cada piloto
alo_lap = session.laps.pick_driver(driver_1).pick_fastest()
ham_lap = session.laps.pick_driver(driver_2).pick_fastest()

#obtenemos el color de cada equipo
ast_color = fastf1.plotting.team_color('RED')
mer_color = fastf1.plotting.team_color('AST')


#cogemos la info del coche
alo_tel = alo_lap.get_car_data().add_distance()
ham_tel = ham_lap.get_car_data().add_distance()

print(alo_tel)


delta_time, ref_tel, compare_tel = utils.delta_time(alo_lap, ham_lap)

plot_ratios = [6, 2, 2, 2, 2, 2]

plt.style.use('dark_background')
plt.rcParams.update({"axes.grid" : True, "grid.color": "#303030", "grid.linestyle": "--"})
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['axes.edgecolor'] = 'white'

print(alo_lap)
# Create subplots with different sizes
plot_size = [15,15]
plt.rcParams['figure.figsize'] = plot_size
plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver_1} VS {driver_2}"
plot_filename = plot_title.replace(" ", "") + ".png"

fig, axs = plt.subplots(6, gridspec_kw={'height_ratios': plot_ratios})


axs[0].plot(alo_tel['Distance'], alo_tel['Speed'], ast_color, label=driver_1 + '  '  + str(alo_lap['LapTime'])[11:19])
axs[0].plot(ham_tel['Distance'], ham_tel['Speed'], mer_color, label=driver_2 + '  '  + str(ham_lap['LapTime'])[11:19])

axs2 = axs[0].twinx()
axs2.plot(ref_tel['Distance'], delta_time, color='white', label='Delta', linestyle='dashed')

axs[0].set(ylabel='KM/H')

axs[0].legend()
axs[0].legend(loc='lower right')

axs[0].set_title(plot_title)

axs2.set(ylabel='Delta (s)')

# Agregar información sobre el acelerador
axs[1].plot(alo_tel['Distance'], alo_tel['Throttle'], ast_color, label=driver_1)
axs[1].plot(ham_tel['Distance'], ham_tel['Throttle'], mer_color, label=driver_2)
axs[1].set(ylabel='Acelerador %')

#Agregar informacion sobre los RPM
axs[2].plot(alo_tel['Distance'], alo_tel['RPM'], ast_color, label=driver_1)
axs[2].plot(ham_tel['Distance'], ham_tel['RPM'], mer_color, label=driver_2)
axs[2].set(ylabel='RPM')

axs[3].plot(alo_tel['Distance'], alo_tel['Brake'], ast_color, label=driver_1)
axs[3].plot(ham_tel['Distance'], ham_tel['Brake'], mer_color, label=driver_2)
axs[3].set(ylabel='Brake')

# Agregar información sobre la marcha
axs[4].plot(alo_tel['Distance'], alo_tel['nGear'], ast_color, label=driver_1)
axs[4].plot(ham_tel['Distance'], ham_tel['nGear'], mer_color, label=driver_2)
axs[4].set(ylabel='nGear')

# Agregar información sobre DRS
axs[5].plot(alo_tel['Distance'], alo_tel['DRS'], ast_color, label=driver_1)
axs[5].plot(ham_tel['Distance'], ham_tel['DRS'], mer_color, label=driver_2)
axs[5].set(ylabel='DRS')

for a in axs.flat:
    a.label_outer()

# Load the image
image = plt.imread(r'C:\Users\jorge\Desktop\fastf1\script_qualy\logo-graf-blanco.png')

# Create an OffsetImage with the image and desired opacity
imagebox = OffsetImage(image, zoom=0.5, alpha=0.18)

# Get the current axes limits
xlim = plt.xlim()
ylim = plt.ylim()

# Compute the center of the y-axis
ycenter = ylim[0] / 3

# Compute half of the maximum x-value
xcenter = xlim[1] / 2

# Create an AnnotationBbox with the OffsetImage and desired position
ab = AnnotationBbox(imagebox, (xcenter, ycenter), frameon=False)

# Add the AnnotationBbox to the current axes
plt.gca().add_artist(ab)

# Your existing code
plt.savefig(plot_filename, dpi=300)
plt.show()