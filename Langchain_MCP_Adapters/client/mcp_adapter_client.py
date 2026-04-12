import asycnio
import os
import sys
import json
from contextlib import AsyncExitStack
from typing import Optional, List

#MCP Client Imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#Agent and LLM Imports
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

#custom json encoder

class CustomEncoder(json.JSONEncoder):

    """
    Custom JSON encoder that handles objects with a content attribute.

    If an object has a "content" attribute, it returns a dictionary with the object's type and it's content.
    Otherwise, it falls back to the default encoding.
    
    """
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)
    
#LLM Instantiation 

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    max_retries=2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

#MCP Server Parameters

if len(sys.argv) < 2:
    print("Uage: python mcp_adapter_client.py <path_to_server_script")
    sys.exit(1)

server_script =sys.argv[1]

server_params = StdioServerParameters(
    command="python" if server_script.endswith(".py") else "node",
    args=[server_script]
)


