import os
import sys
import re 
import json
import googlemaps
#from datetime import datetime
from fastmcp import FastMCP

from typing import Optional, Dict, Any


#-------------
# settings
#-------------
google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=google_maps_api_key)
allowed_modes = ["driving", "walking", "bicycling", "transit"]


#-------------
# helpers
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
# directions
#-------------
class DirectionTools:
    """
    A collection of Google Maps tools for getting directions between 2 locations on a map.
    """

    def directions(origin: str, destination: str, mode: str="driving") -> Optional[Dict[str, Any]]:
        """Gives step-by-step instructions to get from origin to destination uisng a particular mode of transport
        Args:
            origin (str): originating address
            destination (str): destination address
            mode (str, optional): mode of transportation. Valid options are: driving, walking, bicycling, transit

        Returns:
            dictionary (JSON) of steps along with total distance and total duration
        """
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
            return json.dumps(output, separators=(',', ':'))
        else:
            return "No directions found for the specified locations."
