import matplotlib.pyplot as plt
import fastf1.plotting

fastf1.Cache.enable_cache(r'C:\Users\jorge\Desktop\fastf1\cache') # optional

fastf1.plotting.setup_mpl()

session = fastf1.get_session(2023, 'Monaco', 'FP2')
laps = session.load_laps(with_telemetry=True)

# Select laps from specific drivers
alo_lap = session.laps.pick_driver('VER').pick_fastest()
ham_lap = session.laps.pick_driver('ALO').pick_fastest()
ver_lap = session.laps.pick_driver('LEC').pick_fastest()

rbr_color = fastf1.plotting.team_color('RBR')
mer_color = fastf1.plotting.team_color('AST')
ast_color = fastf1.plotting.team_color('FER')

alo_tel = alo_lap.get_car_data().add_distance()
ver_tel = ver_lap.get_car_data().add_distance()
ham_tel = ham_lap.get_car_data().add_distance()

# Calculate delta
ver_tel['Delta'] = ver_tel['Time'] - ver_tel['Time']
alo_tel['Delta'] = alo_tel['Time'] - ver_tel['Time']
ham_tel['Delta'] = ham_tel['Time'] - ver_tel['Time']

fig, ax = plt.subplots(3, 1)
ax[0].plot(ver_tel['Distance'], ver_tel['Speed'], color=rbr_color, label='VER')
ax[0].plot(ham_tel['Distance'], ham_tel['Speed'], color=mer_color, label='HAM')
ax[0].plot(alo_tel['Distance'], alo_tel['Speed'], color=ast_color, label='ALO')

ax[0].set_xlabel('Distance in m')
ax[0].set_ylabel('Speed in km/h')

ax[1].plot(ver_tel['Distance'], ver_tel['Delta'], color=rbr_color, label='VER')
ax[1].plot(ham_tel['Distance'], ham_tel['Delta'], color=mer_color, label='HAM')
ax[1].plot(alo_tel['Distance'], alo_tel['Delta'], color=ast_color, label='ALO')
ax[1].set_xlabel('Distance in m')
ax[1].set_ylabel('Delta in s')

plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()