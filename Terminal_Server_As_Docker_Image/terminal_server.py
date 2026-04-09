import os
import subprocess

from mcp.server.fastmcp import FastMCP

working_dir = "D:\\MCP_Works\\Terminal_Server_As_Docker_Image"
mcp = FastMCP("terminal_cmd_server")

@mcp.tool()
async def run_command(command:str)->str:
    """
    DocString:
    This function takes terminal commands as input and executes it using this tool in given working_dir only.
    Before executing it will say that it is going to use this tool and return
    either command output along with command error if any.

    Arguments:
    command: command to be executed

    Returns:
    Either command output or error
    """
    try:
        result = subprocess.run(command, cwd=working_dir, shell=True, text=True, capture_output=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)
    
if __name__=="__main__":
    mcp.run(transport="stdio")

