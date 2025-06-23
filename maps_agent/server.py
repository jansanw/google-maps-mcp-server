"""This module defines a FastMCP server for Google Maps Platform operations."""
import os
import re
import json
import asyncio
import googlemaps
from datetime import datetime
from fastmcp import FastMCP

from typing import Optional, Dict, Any

#try:
#    from gmaps.directions import DirectionTools
    #from .gmaps.places import find_place, place_nearby, place_details
#except ImportError as e:
#    print(f"[SERVER INIT] ImportError: {e}")


#---------------
# settings
#---------------
# Host for the FastMCP server
host=os.environ.get("FASTMCP_HOST", "0.0.0.0")
# Port for the FastMCP server
port=os.environ.get("FASTMCP_PORT", 8080)
# Transport protocol for the FastMCP server (e.g., stdio, streamable-http, sse)
transport=os.environ.get("FASTMCP_TRANSPORT", "stdio")

google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=google_maps_api_key)


#-------------
# helpers
#-------------
allowed_modes = ["driving", "walking", "bicycling", "transit"]

def assert_mode(mode: str):
    assert mode in allowed_modes, f"ERROR: '{mode}' is not one of the allowed modes: {allowed_modes}"


def strip_html_regex(html_text: str) -> str:
    """Strips HTML tags and reduce multiple blank spaces to one"""
    clean = re.compile('<.*?>')
    temp = re.sub(clean, ' ', html_text)
    final = re.sub(r' {2,}', ' ', temp)
    return final


#-------------
# main
#-------------
# https://gofastmcp.com/servers/fastmcp#server-configuration
# Initialize FastMCP server
mcp = FastMCP(
    name="FastMCP Google Maps Platform Server",
    dependencies=["googlemaps==4.10.0", "asyncio==3.4.3"],
    on_duplicate_tools="error",
)

@mcp.tool()
def get_directions(origin: str, destination: str, mode: str="driving") -> Optional[Dict[str, Any]]:
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
        #return json.dumps(output, indent=4)
        return json.dumps(output, separators=(',', ':'))
    else:
        return "No directions found for the specified locations."


# https://gofastmcp.com/deployment/running-server
if __name__ == "__main__":
    try:
        asyncio.run(mcp.run(transport=transport, host=host, port=port))
    except KeyboardInterrupt:
        print("> FastMCP Google Maps Server stopped by user.")
    except Exception as e:
        print(f"> FastMCP Google Maps Server encountered error: {e}")
    finally:
        print("> FastMCP Google Maps Server exiting.")
