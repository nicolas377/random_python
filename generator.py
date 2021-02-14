import math, json, os, urllib.request, re

os.system('cls')

airportspathslist = ["json/airports.json",
                    "airports.json",
                    os.path.expanduser("~")+"/Downloads/"+"airports.json"]
navdatapathslist = ["json/nav_data.json",
                    "nav_data.json",
                    os.path.expanduser("~")+"/Downloads/"+"nav_data.json"]

def datahandler(pathslist, dataname, text):
    for i in pathslist:
        if os.path.exists(i):
            with open(i, 'rt') as data_json:
                data = json.loads(data_json.read())
            break
    else:
        try:
            with urllib.request.urlopen(f'https://raw.githubusercontent.com/nicolas377/hosting/master/fmc-gen/{dataname}.json') as response:
                data_json = response.read()
                data = json.loads(data_json)
        except:
            print("Sorry, the download failed. Check your internet connection and try again.")
        print(f"Would you like to save the list of {dataname} to the current directory?")
        print("Enter y to save, or leave blank to not save")
        saveq = input()
        if saveq.lower() == "y":
            if os.path.exists("json") == False:
                os.mkdir("json")
            with open(pathslist[0], "w") as f:
                f.write(str(json.dumps(data)))
    return data

def dms2dec(dms_str):
    dms_str = re.sub(r'\s', '', dms_str)

    sign = -1 if re.search('[swSW]', dms_str) else 1

    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else '0'
    second = numbers[2] if len(numbers) >= 3 else '0'
    frac_seconds = numbers[3] if len(numbers) >= 4 else '0'

    second += "." + frac_seconds
    return round((sign * (int(degree) + float(minute) / 60 + float(second) / 3600)), 6)

def manual_coords(name):
    print(f"Point {name} was not found in the database, please enter location manually")
    full = input("Do you want to input a full DMS string?\nEnter y or n.\n> ")
    if full.lower() == "n":
        while True:
            lat = input("Latitude:\n>")
            if "°" in lat:
                lat = dms2dec(str(lat))
            try:
                lat = float(lat)
                break
            except ValueError:
                print("Please enter a valid number")
        while True:
            lon = input("Longitude:\n>")
            if "°" in lon:
                lon = dms2dec(str(lon))
            try:
                lon = float(lon)
                break
            except ValueError:
                print("Please enter a valid number")
    else:
        while True:
            str = input("Full String\n> ")
            dms = str.split()
            lat = dms[0].replace("\\", "")
            lon = dms[1].replace("\\", "")
            lat = dms2dec(lat)
            lon = dms2dec(lon)
            try:
                lat = float(lat)
                break
            except ValueError:
                print("Please enter a valid latitude")
            try:
                lon = float(lon)
                break
            except ValueError:
                print("Please enter a valid longitude")
    return lat, lon

def airport_coords(icao):
    if icao in airports:
        lat = float(airports[icao][0])
        lon = float(airports[icao][1])
    else:
        lat, lon = manual_coords(str(icao))
    return lat, lon

def add_waypoint(waypoint_name, id):
    if waypoint_name.upper() in waypoints:
        lat = float(waypoints[waypoint_name][0][0])
        lon = float(waypoints[waypoint_name][0][1])
    else:
        lat, lon = manual_coords(str(waypoint_name))

    wp['name'] = waypoint_name
    wp['lat'] = lat
    wp['lon'] = lon
    wp['alt'] = None # will be changed later
    wp['in_db'] = False
    wp['notes'] = None # will be changed later

    waypoint_list_wid[id] = wp

def idselect():
    pass

def update():
    altchoice = input("Would you like to update VNAV altitudes?\nEnter yes or no.\n>").lower()
    if altchoice.startswith("y"):
        id = idselect()
        current = waypoint_list_wid[id]
        alt = input("What altitude would you like the VNAV altitude to be?\n>")

def intro():
    # departure
    dep = input("departure airport ICAO code\n>").upper()
    dep_coords = airport_coords(dep)
    lat_dep = dep_coords[0]
    lon_dep = dep_coords[1]

    # arrival
    arr = input("arrival airport ICAO code\n>").upper()
    arr_coords = airport_coords(arr)
    lat_arr = arr_coords[0]
    lon_arr = arr_coords[1]

    # flight number
    fltnbr = input("type flight number, or leave blank to skip\n>").upper()
    return dep, lat_dep, lon_dep, arr, lat_arr, lon_arr, fltnbr

def main_menu():
    while True:
        try:
            points = input("Enter your waypoints\n>").upper()
            seperator = input("What seperates the waypoints?\n>")
            names_list = points.split(seperator)
            break
        except:
            print("There was an error. Please try again.\n")
    return names_list

def main():

    global lat_dep
    global lon_dep
    global lat_arr
    global lon_arr
    global airports
    global waypoints
    global route
    global waypoint_list_wid
    global wp

    wp = {}
    airports = datahandler(airportspathslist, "airports", "airports")
    waypoints = datahandler(navdatapathslist, "waypoints", "waypoints")

    dep, lat_dep, lon_dep, arr, lat_arr, lon_arr, fltnbr = intro()

    num = 1

    route = {}

    waypoint_list_wid = {}

    waypoint_list = main_menu()

    for i in waypoint_list:
        add_waypoint(i, num)
        num += 1

    print(json.dumps(waypoint_list_wid))

main()
