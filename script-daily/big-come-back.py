import requests

url = "https://ergast.com/api/f1/current/driverStandings.json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    drivers = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
    driver_data = []

    for driver in drivers:
        driver_id = driver["Driver"]["driverId"]
        driver_name = driver["Driver"]["givenName"] + " " + driver["Driver"]["familyName"]
        url = f"https://ergast.com/api/f1/drivers/{driver_id}/results.json?limit=1000"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            races = data["MRData"]["RaceTable"]["Races"]
            max_gain = 0

            for race in races:
                grid_pos = int(race["Results"][0]["grid"])
                finish_pos = int(race["Results"][0]["position"])
                gain = grid_pos - finish_pos

                if gain > max_gain:
                    max_gain = gain
                    race_name = race["raceName"]
                    year = race["season"]
                    round_num = race["round"]
                    start_pos = grid_pos
                    end_pos = finish_pos
                    wins = start_pos - end_pos

            driver_data.append((driver_name, max_gain, start_pos, end_pos, wins, race_name, year, round_num))

    driver_data = sorted(driver_data, key=lambda x: x[4], reverse=True)

    for driver in driver_data:
        driver_name, max_gain, start_pos, end_pos, wins, race_name, year, round_num = driver
        print(f"{driver_name}: {max_gain} ({start_pos} -> {end_pos}) - Ganó {wins} posiciones en {race_name} ({year}, ronda {round_num})")

else:
    print("Error")
