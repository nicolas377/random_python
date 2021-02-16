import math, json, os, urllib.request, re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from operator import itemgetter

os.system('cls')

airportspathslist = ["json/airports.json",
                    "airports.json",
                    os.path.expanduser("~")+"/Downloads/"+"airports.json"]
navdatapathslist = ["json/nav_data.json",
                    "nav_data.json",
                    os.path.expanduser("~")+"/Downloads/"+"nav_data.json"]

def datahandler(pathslist, dataname):
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
    print(f"{name} was not found in the database, please enter location manually")
    full = input("Do you want to input a full DMS string?\nEnter y or n.\n>")
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
            str = input("Full String\n>")
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

def add_new_waypoint(waypoint_name, id):
    if waypoint_name.upper() in waypoints:
        coords = waypoints[waypoint_name][0]
        lat = float(coords[0])
        lon = float(coords[1])
    else:
         lat, lon = manual_coords(str(waypoint_name))

    wp = {}

    wp['name'] = waypoint_name
    wp['lat'] = lat
    wp['lon'] = lon
    wp['alt'] = None # will be changed later
    wp['in_db'] = False
    wp['notes'] = None # will be changed later

    waypoint_list_wid[id] = wp

def converttoroute(pre_route, dep, arr, fltnum):
    wplist = []

    route = []

    route.append(dep)
    route.append(arr)
    route.append(fltnum)
    for i in waypoint_list_wid:
        wp = []
        this = waypoint_list_wid[i]
        wp.append(this['name'])
        wp.append(this['lat'])
        wp.append(this['lon'])
        wp.append(this['lat'])
        wp.append(this['alt'])
        wp.append(this['in_db'])
        wp.append(this['notes'])
        wplist.append(wp)
    route.append(wplist)

    route = json.dumps(route)

    return route

def idselect():
    dash = '-' * 75

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

def options():

    # Altitudes
    altchoice = input("Would you like to update VNAV altitudes?\nEnter yes or no.\n>").lower()
    if altchoice.startswith("y"):
        while True:
            id = idselect()
            current = waypoint_list_wid[round(float(id))]
            print(f'Name: {current["name"]}')
            alt = input("What altitude would you like the VNAV altitude to be?\n>")
            current['alt'] = round(round(float(alt), -1))
            waypoint_list_wid[id] = current

            cont = input("Would you like to move to another waypoint?\nEnter yes or no.\n>").lower()
            if cont.startswith('n'):
                break

    # Notes
    noteschoice = input("Would you like to update notes?\nEnter yes or no.\n>").lower()
    if noteschoice.startswith("y"):
        while True:
            id = idselect()
            current = waypoint_list_wid[round(float(id))]
            print(f'Name: {current["name"]}')
            note = input("What altitude would you like the VNAV altitude to be?\n>")
            current['notes'] = str(note)
            waypoint_list_wid[id] = current

            cont = input("Would you like to move to another waypoint?\nEnter yes or no.\n>").lower()
            if cont.startswith('n'):
                break

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
            seperator = input("What separates the waypoints?\n>")
            names_list = points.split(seperator)
            break
        except:
            print("There was an error. Please try again.\n")
    return names_list

# KML functions

def leg_dist(lat0, lon0, lat, lon):

    R = 3441.036714  # this is in nautical miles.

    dLat = math.radians(lat - lat0)
    dLon = math.radians(lon - lon0)
    lat0_rad = math.radians(lat0)
    lat_rad = math.radians(lat)

    a = math.sin(dLat/2)**2 + math.cos(lat0_rad) \
        * math.cos(lat_rad) * math.sin(dLon/2)**2

    c = 2*math.asin(math.sqrt(a))

    return R * c

def Extract(lst):
    return list( map(itemgetter(0), lst ))

def add_waypoint(waypoint, lat, lon, alt, notes, root):
    placemark = ET.Element("Placemark")
    name = ET.SubElement(placemark, "name")
    name.text = waypoint
    description = ET.SubElement(placemark, "description")
    description.text = notes
    point = ET.SubElement(placemark, "Point")
    coordinates = ET.SubElement(point, "coordinates")
    if alt is None:
        coordinates.text = f"{lon},{lat}"
    else:
        coordinates.text = f"{lon},{lat},{alt}"
    root.append(placemark)
    return root

def add_leg(lat0, lon0, lat, lon, leg_name, root):
    placemark = ET.Element("Placemark")
    name = ET.SubElement(placemark, "name")
    name.text = leg_name
    linestring = ET.SubElement(placemark, "LineString")
    coordinates = ET.SubElement(linestring, "coordinates")
    coordinates.text = f"{lon0},{lat0}  {lon},{lat}"
    root.append(placemark)
    return root

def generate_kml(dumpfilename, route_dict, insert_arr, coords_dep, coords_arr):
    # KML header
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    root = ET.SubElement(kml, "Document")

    # dep
    lat_dep = coords_dep[0]
    lon_dep = coords_dep[1]

    # arr
    lat_arr = coords_arr[0]
    lon_arr = coords_arr[1]

    lat0 = lat_dep
    lon0 = lon_dep
    waypoint = route_dict[0]
    root = add_waypoint(waypoint, lat0, lon0, "0", "Departure airport", root)

    # waypoints and legs

    for i in route_dict[3]:
        # waypoint
        waypoint = i[0]
        lat = i[1]
        lon = i[2]
        alt = i[3]
        notes = i[5]
        root = add_waypoint(waypoint, lat, lon, alt, notes, root)

        # leg
        distance = round(leg_dist(lat0, lon0, lat, lon), 1)
        distance = str(distance) + " nm"
        root = add_leg(lat0, lon0, lat, lon, distance, root)

        # and update for next iteration
        lat0 = lat
        lon0 = lon

    # only add arrival if needed
    if insert_arr:
        lat = lat_arr
        lon = lon_arr
        waypoint = route_dict[1]
        root = add_waypoint(waypoint, lat, lon, "0", "Arrival airport", root)
        distance = round(leg_dist(lat0, lon0, lat, lon), 1)
        distance = str(distance) + " nm"
        root = add_leg(lat0, lon0, lat, lon, distance, root)

    doc = minidom.parseString(ET.tostring(kml))
    open(dumpfilename, "x")
    with open(dumpfilename, "w") as dumpfile:
        dumpfile.write(doc.toprettyxml())
        dumpfile.close()

def airportCoords(airport):
    if airport in airports:
        lat = airports[airport][0]
        lon = airports[airport][1]
    else:
        lat, lon = manual_coords(str(airport))
    return lat, lon

def convertandsave(route):

    rte = json.loads(route)

    dep = rte[0]
    coords_dep = airportCoords(dep)

    arr = rte[1]
    coords_arr = airportCoords(arr)

    waypoints_list = rte[3]

    for waypoint in waypoints_list:
        waypoint_name = waypoint[0]
        lat = waypoint[1]
        lon = waypoint[2]

    if any('RW' in s for s in Extract(waypoints_list[-2:])):
        insert_arr = False
    else:
        insert_arr = True

    # Save the route

    dumpfilename = "routes/" + f'{rte[0]}{rte[1]}/' + 'route' + ".kml"
    generate_kml(dumpfilename, rte, insert_arr, coords_dep, coords_arr)

def finalize():
    if not os.path.isdir('routes'):
        os.mkdir('routes')
    rte = json.loads(route)
    path = f'routes/{rte[0]}{rte[1]}'
    if not os.path.isdir(path):
        os.mkdir(path)
    convertandsave(route)
    open(f'routes/{rte[0]}{rte[1]}/route.txt', "x")
    with open(f'routes/{rte[0]}{rte[1]}/route.txt', "w") as dumpfile:
        dumpfile.write(route)
        dumpfile.close()


def main():

    global lat_dep
    global lon_dep
    global lat_arr
    global lon_arr
    global airports
    global waypoints
    global route
    global waypoint_list_wid

    airports = datahandler(airportspathslist, "airports")
    waypoints = datahandler(navdatapathslist, "waypoints")

    dep, lat_dep, lon_dep, arr, lat_arr, lon_arr, fltnbr = intro()

    num = 1

    route = []

    waypoint_list_wid = {}

    waypoint_list = main_menu()

    for i in waypoint_list:
        add_new_waypoint(i, num)
        num += 1

    options()

    route = converttoroute(waypoint_list_wid, dep, arr, fltnbr)

    finalize()

    print("Route and KML saved")

main()
