import asyncio
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
    print("Usage: python mcp_adapter_client.py <path_to_server_script>")
    sys.exit(1)

server_script=sys.argv[1]

server_params = StdioServerParameters(
    command="python" if server_script.endswith(".py") else "node",
    args=[server_script]
)

mcp_client=None

#Main async function run_agent

async def run_agent():
    """
    connect to the mcp server, load mcp tools, create a react agent, and run an interactive chat loop.
    
    steps:
    open a stdio connection to mcp server
    create and initialize mcp session
    store the session in a global holder (mcp_client) for tools access
    load mcp tools using load_mcp_tools
    create agent using create_agent with LLM and loaded tools
    enter an interactive loop : for each user query, invoke the agent asynchronously using ainvoke then print
    the response as formatted JSON using custom encoder
    
    """
    global mcp_client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write)as session:
            await session.initialize()

            mcp_client = type("MCPClientHolder", (), {"session": session})()

            tools = await load_mcp_tools(session)

            agent = create_agent(llm, tools)
            print("MCP Client Started! Type 'quit' to exit")
            while True:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                response = await agent.ainvoke({"messages":{"role":"user", "content": query}})

                try:
                    formatted = json.dumps(response, indent=2, cls=CustomEncoder)
                except Exception as e:
                    formatted = str(response)
                print("\nResponse:")
                print(formatted)        

    return 

if __name__=="__main__":
    asyncio.run(run_agent())