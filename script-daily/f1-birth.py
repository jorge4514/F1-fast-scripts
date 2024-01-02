import requests
from datetime import datetime

# Ejemplo de solicitud GET al Ergast Developer API para obtener la lista de carreras de Fórmula 1 y filtrar los resultados para mostrar solo las carreras que cumplen años en este día
response = requests.get('http://ergast.com/api/f1/races.json?limit=1000')
data = response.json()
races = data['MRData']['RaceTable']['Races']
today = datetime.now()
month = today.month
day = today.day
races_today = [race for race in races if datetime.strptime(race['date'], '%Y-%m-%d').month == month and datetime.strptime(race['date'], '%Y-%m-%d').day == day]
for race in races_today:
    print(race['season'], race['raceName'])
    results_url = f"http://ergast.com/api/f1/{race['season']}/{race['round']}/results.json"
    response = requests.get(results_url)
    data = response.json()
    results = data['MRData']['RaceTable']['Races'][0]['Results']
    drivers = [result['Driver']['givenName'] + ' ' + result['Driver']['familyName'] for result in results]
    positions = [result['positionText'] for result in results]
    if 'Fernando Alonso' in drivers:
        index = drivers.index('Fernando Alonso')
        position = positions[index]
        print(f'Fernando Alonso participó en esta carrera y quedó en la posición {position}')
        if position in ['1', '2', '3']:
            driver_id = 'alonso'
            response = requests.get(f'http://ergast.com/api/f1/drivers/{driver_id}/results.json?limit=1000')
            data = response.json()
            results = data['MRData']['RaceTable']['Races']
            podiums = 0
            for result in results:
                if int(result['season']) > int(race['season']) or (int(result['season']) == int(race['season']) and int(result['round']) >= int(race['round'])):
                    break
                position = result['Results'][0]['positionText']
                if position in ['1', '2', '3']:
                    podiums += 1
            years_ago = today.year - int(race['season'])
            print(f'Este fue el podio número {podiums + 1} de Fernando Alonso y fue hace {years_ago} años')
    if 'Carlos Sainz' in drivers:
        index = drivers.index('Carlos Sainz')
        position = positions[index]
        print(f'Carlos Sainz participó en esta carrera y quedó en la posición {position}')
        if position in ['1', '2', '3']:
            driver_id = 'sainz'
            response = requests.get(f'http://ergast.com/api/f1/drivers/{driver_id}/results.json?limit=1000')
            data = response.json()
            results = data['MRData']['RaceTable']['Races']
            podiums = 0
            for result in results:
                if int(result['season']) > int(race['season']) or (int(result['season']) == int(race['season']) and int(result['round']) >= int(race['round'])):
                    break
                position = result['Results'][0]['positionText']
                if position in ['1', '2', '3']:
                    podiums += 1
            years_ago = today.year - int(race['season'])
            print(f'Este fue el podio número {podiums + 1} de Carlos Sainz y hace {years_ago} años de eso')
