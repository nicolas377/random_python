import os, json, math, urllib.request
import xml.etree.ElementTree as ET
from operator import itemgetter
from xml.dom import minidom
from glob import glob

airportspathslist = ["json/airports.json",
                    "airports.json",
                    os.path.expanduser("~")+"/Downloads/"+"airports.json"]

if not os.path.exists("routes"):
    os.mkdir("routes")
    print("Make sure your routes are in the routes folder")

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

airports = datahandler(airportspathslist, "airports")
files = os.listdir('routes')
txt_files = []
kml_files = []
conversion_queue = []
files_converted = 0
paths = str(glob('*/'))
subdir_list_1 = paths.replace('//', '')
subdir_list = subdir_list_1.replace('\\', '')
path = []

# Converting functions

# calculate between-waypoint leg distance with Haversine formula
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

def airportCoords(airport):
    if airport in airports:
        lat = airports[airport][0]
        lon = airports[airport][1]
    else:
        print(f"{airport} is not in database, please enter location manually")
        lat = float(input("Latitude:\n"))
        lon = float(input("Longitude:\n"))
    return lat, lon

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

    # only add arrival if specified by user
    if insert_arr:
        lat = lat_arr
        lon = lon_arr
        waypoint = route_dict[1]
        root = add_waypoint(waypoint, lat, lon, "0", "Arrival airport", root)
        distance = round(leg_dist(lat0, lon0, lat, lon), 1)
        distance = str(distance) + " nm"
        root = add_leg(lat0, lon0, lat, lon, distance, root)

    doc = minidom.parseString(ET.tostring(kml))
    with open(dumpfilename, "wb") as dumpfile:
        dumpfile.write(doc.toprettyxml(encoding='utf-8'))
        dumpfile.close()

def convert(loadfilepath1):
    loadfilepath = "routes/" + str(loadfilepath1) + ".txt"

    with open(loadfilepath, "r") as routefile:
        route_dict = json.load(routefile)

    dep = route_dict[0]
    coords_dep = airportCoords(dep)

    arr = route_dict[1]
    coords_arr = airportCoords(arr)

    waypoints_list = route_dict[3]

    for waypoint in waypoints_list:
        waypoint_name = waypoint[0]
        lat = waypoint[1]
        lon = waypoint[2]

    if any('RW' in s for s in Extract(waypoints_list[-2:])):
        insert_arr = False
    else:
        insert_arr = True

    dumpfilename = "routes/" + loadfilepath1 + ".kml"
    generate_kml(dumpfilename, route_dict, insert_arr, coords_dep, coords_arr)
if __name__ == "__main__":
   for x in files:
       if x[-4:] == ".txt":
           x_nfe = x.replace('.txt', '')
           txt_files.append(x_nfe)
       if x[-4:] == ".kml":
           x_nfe = x.replace('.kml', '')
           kml_files.append(x_nfe)

   for i in txt_files:
       if i not in kml_files:
           conversion_queue.append(i)

   if any(conversion_queue):
       for x in conversion_queue:
           convert(x)
           files_converted += 1
       print(str(files_converted) + " files converted")
   else:
       print("0 files converted")
