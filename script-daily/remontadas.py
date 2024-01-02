import requests

for year in range(1991, 2023):
    url = f"https://ergast.com/api/f1/{year}/circuits/catalunya/results.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data["MRData"]["RaceTable"]["Races"][0]["Results"]
        remontadas = []
        for result in results:
            grid = int(result["grid"])
            position = int(result["position"])
            if position < grid and position <= 3:
                remontadas.append((grid, position))
        remontadas.sort(key=lambda x: x[1] - x[0], reverse=True)
        if len(remontadas) > 0:
            print(f"Resultados de la carrera de Cataluña en {year}:")
            for i in range(min(10, len(remontadas))):
                print(f"Posición en parrilla: {remontadas[i][0]}, posición final: {remontadas[i][1]}")
        else:
            print(f"No hubo pilotos que terminaran en las posiciones 1, 2 o 3 en la carrera de Cataluña en {year}.")
    else:
        print(f"Error al obtener los datos para el año {year}.")

