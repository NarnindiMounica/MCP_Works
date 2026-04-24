from mcp.server.fastmcp import FastMCP
from tools.weather import get_weather


mcp = FastMCP("Weather Checker")

@mcp.tool()
async def check_weather(location:str)->str
    """get weather information for a specified location"""
    return get_weather(location)

if __name__=="__main__":
    mcp.run(transport="stdio")
        
