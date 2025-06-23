import os
import asyncio
from contextlib import AsyncExitStack

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


#-----------------
# settings
#-----------------
# Model to be used by the agent
model="gemini-2.5-flash"
google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY")


#-----------------
# agents
#-----------------
maps_agent = LlmAgent(
    name="maps_agent",
    model=model,
    instruction=(
        "You are a helpful AI assistant designed to provide map directions. Only use the tools you are provided to assist the user."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='fastmcp',
                args=[
                    "run",
                    "maps_agent/server.py"
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key
                },
            ),
            #tool_filter=['tool1', 'tool2']
        )
        
    ],
)

root_agent = maps_agent
