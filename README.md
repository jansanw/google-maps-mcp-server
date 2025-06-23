# google-maps-mcpserver
Google Maps Platform MCP server


## FastMCP
This part is pretty straightforward:
```sh
python ./server.py
```
or
```sh
fastmcp run server.py --transport stdio
```

**NOTE:** if you use the `fastmcp` option, it ignores the `if __name__ == "__main__"`, so you need to pass `--transport` and `--port
