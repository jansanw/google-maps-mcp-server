import os
import re 
import json
import googlemaps

from typing import Optional, Dict, Any


#-------------
# settings
#-------------
google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=google_maps_api_key)
allowed_input_types = ["textquery", "phonenumber"]


#-------------
# helper
#-------------
def assert_input_type(input_type: str):
    assert input_type in allowed_input_types, f"ERROR: '{input_type}' is not one of the allowed inpute types: {allowed_input_types}"


#-------------
# mcp
#-------------
def find_place(input: str, input_type: str="textquery", fields: list=["place_id", "formatted_address", "name", "geometry", "types", "rating"]) -> Optional[Dict[str, Any]]:
    """Find/query a place with the provided name
    Args:
        input (str): name of the place you're looking for. provide more details if possible (i.e. city, country, etc.) for better accuracy. can also be the establishment type (i.e. bakery, bank, etc.)
        input_type (str, optional): the type of query, it can be a textquery or phonenumber query
        fields (list, optional): list of fields to query for

    Returns:
        dictionary (JSON) of with basic information of the top result based on input query. basic information inclulde:
        - name
        - place_id
        - address
        - location (latitude, longitude)
        - establishment type
        - average rating
    """
    try:
        assert_input_type(input_type)
    except AssertionError as e:
        print(e)

    results = gmaps.find_place(input, input_type, fields)

    if results:
        try:
            place = results.get('candidates', {})[0]
        except IndexError:
            return "No such place found"

        output = {
            "name": place['name'],
            "place_id": place['place_id'],
            "formatted_address": place['formatted_address'],
            "location": place['geometry']['location'],
            "types": place['types'],
            "rating": place.get('rating', None),
        }
        return json.dumps(output, separators=(',', ':'))


def place_nearby(location: dict, radius: int, place_type: str) -> Optional[Dict[str, Any]]:
    """Find types of places within a radius of a location (latitude, longitude)
    Args:
        location (dict): dictionary with 'lat' and 'lng' as keys and values are the latitude and longitude respectively
        radius (int): search area radius in meters (i.e. 2500 = 2.5km)
        place_type (str): type of place you're looking for (i.e. "italian restaurant", "hotel", etc.)

    Returns:
        dictionary (JSON) of establishment names (key) and their place_id (value)
    """
    results = gmaps.places_nearby(location, radius, place_type)
    output = {}

    if results:
        places_nearby = results.get('results', {})
        #print(f"{len(places_nearby)} results were found")

        for place in range(len(places_nearby)):
            place_name = places_nearby[place]['name']
            place_id = places_nearby[place]['place_id']

            output[place_name] = place_id
            #print(place_details(output[place_name]))

        return json.dumps(output, separators=(',', ':'))
    else:
        return "Nothing nearby that matches the search criteria was found."


def place_details(place_id: str, fields: list=["name", "formatted_address", "formatted_phone_number", "geometry", "website", "types", "rating", "user_ratings_total"]) -> Optional[Dict[str, Any]]:
    """
    Args:
        place_id (str): place_id of the place, which can be obtained via find_place() or place_nearby()
        fields (list, optional): list of fields to query for

    Returns:
        dictionary (JSON) of with details of provided place. details inclulde:
        - name
        - address
        - location (latitude, longitude)
        - phone number
        - website
        - establishment type
        - average rating
        - total rating count
    """
    results = gmaps.place(place_id, fields)

    if results:
        place_details = results.get('result', {})

        output = {
            "name": place_details['name'],
            "formatted_address": place_details['formatted_address'],
            "location": place_details['geometry']['location'],
            "formatted_phone_number": place_details.get('formatted_phone_number', None),
            "website": place_details.get('website', None),
            "types": place_details['types'],
            "rating": place_details.get('rating', None),
            "user_ratings_total": place_details.get('user_ratings_total', 0),
        }
        return json.dumps(output, separators=(',', ':'))
    else:
        return "No such place found."


#print(find_place("Engineering 7, Waterloo"))
print("FIND PLACE")
print(find_place("+14162928742", input_type="phonenumber"))
print(find_place("Googleplex"))
print(find_place("Coffee shop")) # if you don't specify, it will use your current location
print(find_place("My current location"))
#print(find_place("Alton Chinese Restaurant, Scarborough"))
#print(find_place("Tim Horton's near 30 Muirlands Drive"))
#print(find_place("Random temple, Wakanda"))
print("PLACE DETAILS")
print(place_details("ChIJr6vaxLHW1IkRgrdDqsWyvN4"))

print("PLACES NEARBY")
#print(place_nearby({"lat": 43.825212,"lng":-79.27592589999999}, "2000", "italian restaurant"))
print(place_nearby({"lat":43.4730414,"lng":-80.53952389999999}, "1000", "hotel"))
