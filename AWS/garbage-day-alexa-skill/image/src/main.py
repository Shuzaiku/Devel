# import boto3
# import ask_sdk_core
# import shapely
# import arcgis
# import os

from arcgis.gis import GIS
from arcgis.geocoding import geocode
from arcgis.geometry import Geometry, Point
import requests
import os

def handler(event, context):
    # Declare return values
    status_code = ""
    body = ""

    # Load environment variables
    API_KEY = os.environ["API_KEY"]

    # User input
    user_address = "Bel-Air Drive, Ottawa, ON" # This is just a test address

    # API calls
    gis = GIS(api_key=API_KEY)
    request = requests.get("https://services.arcgis.com/G6F8XLCl5KtAlZ2G/arcgis/rest/services/Solid_Waste_Collection_Calendar_Test/FeatureServer/0/query?where=1%3D1&outFields=GCD,SCHEDULE&outSR=4326&f=json")
    if request.status_code != 200:
        status_code = request.status_code
        body = "Invalid API request"
        return {"statusCode": status_code, "body": body}

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
        status_code = 200
        body += f"Garbage info for {user_address}:\n"
        body += f"Garbage collection day: {gcd}\n"
        body += f"Schedule: {schedule == 'A' and schedule_a or schedule_b}"
    else:
        status_code = 500
        body = "Failed to fetch GCD and schedule information from JSON file."

    return {"statusCode": status_code, "body": body}