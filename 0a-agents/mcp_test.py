import mcp_client

our_mcp_client = mcp_client.MCPClient(["python3", "-u", "weather_server.py"])

our_mcp_client.start_server()
our_mcp_client.initialize()
our_mcp_client.initialized()

