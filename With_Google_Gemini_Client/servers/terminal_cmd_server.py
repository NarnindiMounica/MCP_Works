import os
import subprocess

from mcp.server.fastmcp import FastMCP

workspace = "D:\\MCP_Works\\With_Google_Gemini_Client\\workspace"

mcp = FastMCP("terminal_mcp")

@mcp.tool()
async def run_commands(command:str)->str:
    """
    This function takes terminal command as input 
    and executes that in given workspace directory.
    Use only this tool to execute the command, also let user know that you
    are going to execute it using it 
    
    Args:
    command: the terminal command
    
    Returns:
    returns output of command and error message if any"""
    try:
        result = subprocess.run(command, cwd=workspace, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)


if __name__=="__main__":
    mcp.run(transport="stdio")