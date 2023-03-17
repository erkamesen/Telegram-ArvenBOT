import json
import requests
from bs4 import BeautifulSoup
from numpy import sin, cos, arccos, pi, round
import requests
from bs4 import BeautifulSoup
import os

current_path = os.getcwd()
with open(f"{current_path}/earthquake/cities.json", "r") as f:
    cities = json.load(f)


headers = {
    "Host": "www.koeri.boun.edu.tr",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}


res = requests.get("http://www.koeri.boun.edu.tr/scripts/lst6.asp", headers=headers)

soup = BeautifulSoup(res.content, "html.parser")


class Eartquake:
    def __init__(self, date, time, latitude, longitude, depth, MD, ML, MW, location, control):
        self.date = date
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.MD = MD
        self.ML = ML
        self.MW  = MW
        self.location = location
        self.control = control


fetch_earthquakes = soup.pre.text.splitlines()[7:]
earthquake_list = []

for fetched in fetch_earthquakes:
    earthquake = fetched.split()
    if earthquake:
        if "İlksel" in earthquake:
            new_earthquake = Eartquake(date=earthquake[0],
                            time=earthquake[1],
                            latitude=float(earthquake[2]),
                            longitude=float(earthquake[3]),
                            depth=float(earthquake[4]),
                            MD=earthquake[5],
                            ML=earthquake[6],
                            MW=earthquake[7],
                            location=" ".join(earthquake[8:-1]),
                            control=earthquake[-1]
                            )
            earthquake_list.append(new_earthquake)
        else:
            new_earthquake = Eartquake(date=earthquake[0],
                            time=earthquake[1],
                            latitude=float(earthquake[2]),
                            longitude=float(earthquake[3]),
                            depth=float(earthquake[4]),
                            MD=earthquake[5],
                            ML=earthquake[6],
                            MW=earthquake[7],
                            location=" ".join(earthquake[8:-3]),
                            control=" ".join(earthquake[-3:])
                            )
            earthquake_list.append(new_earthquake)


def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

def getDistanceBetweenPointsNew(latitude1, longitude1, city, unit = 'kilometers'):
    
    try:
        latitude2 = float(cities[city]["lat"])
        longitude2 = float(cities[city]["lng"])
    except KeyError:
        return False
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    
    if unit == 'miles':
        return round(distance, 2)
    if unit == 'kilometers':
        return round(distance * 1.609344, 2)


if __name__ == "__main__":
    print(getDistanceBetweenPointsNew(latitude1=39.933365, longitude1=32.859741, city="Karabük"))
    # 139.8