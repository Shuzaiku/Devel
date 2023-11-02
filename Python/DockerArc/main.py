from arcgis.gis import GIS
from arcgis.geocoding import geocode
from arcgis.geometry import Geometry, Point
import requests

# User input
user_address = "Bel-Air Drive, Ottawa, ON" #"443 LeBoutillier Ave, Ottawa, ON"

# API calls
gis = GIS(api_key="AAPK27fb4e16eab3447d88d67bb8d500fce8FN7SCiiWuEyF4_WRFVyy2JtCeM_sYMENhy8pwkhGzCzoHAZsAI2DtnF3Y2QNTbNL")
request = requests.get("https://services.arcgis.com/G6F8XLCl5KtAlZ2G/arcgis/rest/services/Solid_Waste_Collection_Calendar_Test/FeatureServer/0/query?where=1%3D1&outFields=GCD,SCHEDULE&outSR=4326&f=json")
if request.status_code != 200:
    print("Invalid API request")
    exit()

json_dict = request.json()
wkid = json_dict["spatialReference"]["wkid"]

geocode_result = geocode(address=user_address)
location = geocode_result[0]["location"]
pt = Point({"x" : location["x"], "y" : location["y"], "spatialReference" : {"wkid" : wkid}})
gcd = None
schedule = None

schedule_a = ["Green bin", "Garbage", "Blue bin", "Yard trimmings"]
schedule_b = ["Black bin", "Green bin", "Yard trimmings"]

# Search for user location in geometry
for feature in json_dict["features"]:
    geom = Geometry(feature["geometry"])
    is_contained = geom.contains(second_geometry=pt, relation="BOUNDARY")

    if is_contained:
        gcd = feature["attributes"]["GCD"]
        schedule = feature["attributes"]["SCHEDULE"]
        break

# Processing
if gcd and schedule:
    print(f"Garbage info for {user_address}:")
    print("Garbage collection day:", gcd)
    print("Schedule:", schedule == 'A' and schedule_a or schedule_b)
else:
    print("Failed to fetch GCD and schedule information from JSON file.")