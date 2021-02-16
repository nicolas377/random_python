import math, json, os, urllib.request, re

os.system('cls')

waypoint_list_wid = json.loads('{"1": {"name": "RIGNZ", "lat": 39.158963889, "lon": -77.306638889, "alt": null, "in_db": false, "notes": null}, "2": {"name": "JCOBY", "lat": 39.136269444, "lon": -77.172444444, "alt": null, "in_db": false, "notes": null}, "3": {"name": "GRIIM", "lat": 39.106994444, "lon": -76.989, "alt": null, "in_db": false, "notes": null}, "4": {"name": "SOOKI", "lat": 39.118383333, "lon": -76.522286111, "alt": null, "in_db": false, "notes": null}, "5": {"name": "SWANN", "lat": -32.012613889, "lon": 115.819727778, "alt": null, "in_db": false, "notes": null}, "6": {"name": "BROSS", "lat": 39.191222222, "lon": -75.880522222, "alt": null, "in_db": false, "notes": null}, "7": {"name": "STIKY", "lat": 39.279919444, "lon": -75.766319444, "alt": null, "in_db": false, "notes": null}, "8": {"name": "BRAND", "lat": 40.035077778, "lon": -74.735972222, "alt": null, "in_db": false, "notes": null}, "9": {"name": "LAURN", "lat": 40.551613889, "lon": -74.120463889, "alt": null, "in_db": false, "notes": null}, "10": {"name": "NEWES", "lat": 40.855613889, "lon": -73.444936111, "alt": null, "in_db": false, "notes": null}, "11": {"name": "FEXXX", "lat": 41.210983333, "lon": -72.9166, "alt": null, "in_db": false, "notes": null}, "12": {"name": "RUIZE", "lat": 41.479341667, "lon": -72.209427778, "alt": null, "in_db": false, "notes": null}, "13": {"name": "AWLIN", "lat": 41.556244444, "lon": -71.999158333, "alt": null, "in_db": false, "notes": null}, "14": {"name": "BANKI", "lat": 41.595663889, "lon": -71.867675, "alt": null, "in_db": false, "notes": null}, "15": {"name": "ROBUC", "lat": 41.678919444, "lon": -71.585116667, "alt": null, "in_db": false, "notes": null}, "16": {"name": "PROVI", "lat": 41.723738889, "lon": -71.431713889, "alt": null, "in_db": false, "notes": null}, "17": {"name": "JOODY", "lat": 41.785380556, "lon": -71.287563889, "alt": null, "in_db": false, "notes": null}, "18": {"name": "KRANN", "lat": 41.855191667, "lon": -71.123461111, "alt": null, "in_db": false, "notes": null}, "19": {"name": "KLEBB", "lat": 42.108411111, "lon": -70.616133333, "alt": null, "in_db": false, "notes": null}, "20": {"name": "HOKDU", "lat": 42.345536111, "lon": -70.565502778, "alt": null, "in_db": false, "notes": null}, "21": {"name": "AYBEE", "lat": 42.440558333, "lon": -70.527911111, "alt": null, "in_db": false, "notes": null}, "22": {"name": "KLANE", "lat": 42.414105556, "lon": -70.680580556, "alt": null, "in_db": false, "notes": null}, "23": {"name": "LONER", "lat": -24.713333333, "lon": 150.386666667, "alt": null, "in_db": false, "notes": null}, "24": {"name": "RIPIT", "lat": 42.379655556, "lon": -70.877513889, "alt": null, "in_db": false, "notes": null}}')

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
        list1 = waypoint_list_wid[x]
        print("{:<5}{:^9}{:^15}{:^15}{:^11}{:<8}".format(x,
                                                         list1['name'],
                                                         list1['lat'],
                                                         list1['lon'],
                                                         str(list1['alt']),
                                                         str(list1['notes'])))

    id = input("enter id\n>")
    id = round(float(id))
    id = (f"{id}")
    return id

id = idselect()
print(waypoint_list_wid[id])
