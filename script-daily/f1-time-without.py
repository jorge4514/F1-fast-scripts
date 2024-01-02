import requests
from datetime import datetime

def get_time_since_last_win_or_podium(driver_id):
    url = f'http://ergast.com/api/f1/drivers/{driver_id}/results.json?limit=1000'
    response = requests.get(url)
    data = response.json()
    races = data['MRData']['RaceTable']['Races']
    last_win_date = None
    last_podium_date = None
    for race in races:
        if race['Results'][0]['position'] == '1':
            last_win_date = datetime.strptime(race['date'], '%Y-%m-%d')
        elif race['Results'][0]['position'] in ['2', '3']:
            podium_date = datetime.strptime(race['date'], '%Y-%m-%d')
            if last_podium_date is None or podium_date > last_podium_date:
                last_podium_date = podium_date

    time_since_last_win = datetime.now() - last_win_date if last_win_date is not None else None
    time_since_last_podium = datetime.now() - last_podium_date if last_podium_date is not None else None

    return time_since_last_win.days, time_since_last_podium.days

alonso_time_since_last_win, alonso_time_since_last_podium = get_time_since_last_win_or_podium('alonso')
sainz_time_since_last_win, sainz_time_since_last_podium = get_time_since_last_win_or_podium('sainz')

print(f'Fernando Alonso lleva {alonso_time_since_last_win} días sin ganar una carrera y {alonso_time_since_last_podium} días desde su último podio.')
print(f'Carlos Sainz Jr. lleva {sainz_time_since_last_win} días sin ganar una carrera y {sainz_time_since_last_podium} días desde su último podio.')
