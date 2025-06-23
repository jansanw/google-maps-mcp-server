# Google Maps Platform MCP server

## Setup
For this example, you will need a Google Maps Platform API key.  I restricted my APIs to the following:
- Directions API
- Distance Matrix API
- Geocoding API
- Places API

You may need to expand on this if you wish to add more functionality.  Here is the [Google Maps Platform API Picker](https://developers.google.com/maps/documentation/api-picker) to help you decided what you need.  You will also need an set an additional environment variable, `GOOGLE_MAPS_API_KEY`.

Of course, there will be a [cost](https://mapsplatform.google.com/pricing) to using the Maps API as well.  It's got a pretty generous free-tier, depending on what you're using, just don't go crazy with it ;)


## Running the FastMCP server
```sh
fastmcp run server.py --transport stdio
```

You can substitute `stdio` with `streaming-http` or `sse` (deprecated) depending on your deployment method.


**NOTE:** if you use the `fastmcp` option, it ignores the `if __name__ == "__main__"`, so you need to pass `--transport` and any other settings you wish to override.
