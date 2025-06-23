import os
import re 
import json
import googlemaps
from datetime import datetime
from fastmcp import FastMCP

from typing import Optional, Dict, Any


#-------------
# settings
#-------------
google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=google_maps_api_key)
allowed_modes = ["driving", "walking", "bicycling", "transit"]


#-------------
# helper
#-------------
def assert_mode(mode: str):
    assert mode in allowed_modes, f"ERROR: '{mode}' is not one of the allowed modes: {allowed_modes}"


def strip_html_regex(html_text: str) -> str:
    """Strips HTML tags and reduce multiple blank spaces to one"""
    clean = re.compile('<.*?>')
    temp = re.sub(clean, ' ', html_text)
    final = re.sub(r' {2,}', ' ', temp) 
    return final


#-------------
# mcp
#-------------
#@mcp.tool()
def geocoding(address: str, destination: str, mode: str="driving") -> Optional[Dict[str, Any]]:
    """
    Args:

    Returns:
    """
    #url = "https://maps.googleapis.com/maps/api/directions/json"
    try:
        assert_mode(mode)
    except AssertionError as e:
        print(e)

    results = gmaps.directions(origin, destination, mode=mode)

    if results:
        route = results[0]
        
        output = {
            "total_distance": route['legs'][0]['distance']['text'],
            "total_duration": route['legs'][0]['duration']['text'],
            "steps": []
        }

        for leg in route['legs']:
            for step in leg['steps']:
                output["steps"].append({
                    "instruction": strip_html_regex(step['html_instructions']),
                    "distance": step['distance']['text'],
                    "duration": step['duration']['text']
                })
        #return json.dumps(output, indent=4) 
        return json.dumps(output, separators=(',', ':'))
    else:
        return "No directions found for the specified locations."

#print(directions("Toronto, Ontario", "Montreal, QC"))
#print(directions("Toronto, Ontario", "Lisbon, Portugal"))
#print(directions("Engineering 7, Waterloo", "Bulk Barn, 66 Bridgeport Road East, Waterloo"))
#print(directions("Engineering 7, Waterloo", "McCabe's Irish Pub & Grill, Waterloo", "walking"))
print(directions("Engineering 7, Waterloo", "McCabe's Irish Pub & Grill, Waterloo"))
