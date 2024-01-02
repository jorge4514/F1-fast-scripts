import requests

for year in range(1991, 2023):
    url = f"https://ergast.com/api/f1/{year}/circuits/catalunya/results.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data["MRData"]["RaceTable"]["Races"][0]["Results"]
        mejor_remontada = None
        for result in results:
            grid = int(result["grid"])
            position = int(result["position"])
            if position < grid and position <= 3:
                remontada = position - grid
                if mejor_remontada is None or remontada > mejor_remontada[0]:
                    mejor_remontada = (remontada, result["Driver"]["givenName"], result["Driver"]["familyName"])
        if mejor_remontada is not None:
            print(f"La mayor remontada que terminó en las posiciones 1, 2 o 3 en la carrera de Cataluña en {year} fue de {mejor_remontada[0]} posiciones y fue realizada por {mejor_remontada[1]} {mejor_remontada[2]}.")
        else:
            print(f"No hubo pilotos que terminaran en las posiciones 1, 2 o 3 después de haber salido detrás de ellas en la carrera de Cataluña en {year}.")
