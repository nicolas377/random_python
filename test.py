import math, json, os, urllib.request, re

os.system('cls')

waypoint_list_wid = json.loads('{"1": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "2": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "3": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "4": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "5": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "6": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "7": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "8": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "9": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "10": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "11": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "12": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "13": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "14": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "15": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "16": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "17": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "18": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "19": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "20": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "21": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "22": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "23": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}, "24": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}}')

def idselect():
    dash = '-' * 75

    print("Route so far")
    print(dash)
    print("{:<5}{:^9}{:^15}{:^15}{:^11}{:<8}".format("ID",
                                                     "Name",
                                                     "Latitude",
                                                     "Longitude",
                                                     "Altitude",
                                                     "Notes"))
    print(dash)
    for x in waypoint_list_wid:
        print(waypoint_list_wid[x])

    id = input("enter id\n>")
    id = round(float(id))
    id = (f"{id}")
    return id

id = idselect()
print(waypoint_list_wid[id])
