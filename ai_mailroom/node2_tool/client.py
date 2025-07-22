import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from langchain_openai import ChatOpenAI
import sys
import os
from ai_mailroom.myllm  import GetLLM
from langchain.schema import HumanMessage, AIMessage
import re
import json
from collections import namedtuple
from langchain_core.prompts import ChatPromptTemplate
from state import MailRoomState


ToolCall = namedtuple("ToolCall", ["name", "input"])

class MCPClient:


    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
      
        
        


    # methods will go here


    async def connect_to_server(self, server_script_path: str):
      
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env={"PYTHONPATH": "/Users/blakechang/Documents/git/AImaster"}
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()


    # async def chat_loop(self, state: MailRoomState):
    #     """Run an interactive chat loop"""
    #     print("\nMCP Client Started!")
    #     print("Type your queries or 'quit' to exit.")

    #     # while True:
    #     #     try:

    #     response = await self.process_query(state.user_input)
    #         #     print("\n" + response)

    #         # except Exception as e:
    #         #     print(f"\nError: {str(e)}")

    # async def call_tool(self, tool_name: str, tool_args: dict):
    #     pass
    
    async def process_query(self, state: MailRoomState) -> str:
  
        llm_creator = GetLLM(provider="openai")
        llm = llm_creator.get_llm()

        #TODO: bind_tools
         # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])
        openai_tools = [
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema  # MCP's inputSchema becomes OpenAI's parameters
        }
        for tool in tools
        ]
        llm_with_tools = llm.bind_tools(openai_tools)

        prompt = ChatPromptTemplate.from_messages(
            [(
                "system", "only use tools to answer the question, don't answer the question directly"),
                ("human", "{query}")
             ])
        chain = prompt| llm_with_tools
        output = await chain.ainvoke({"query", state.user_input})


        if output.tool_calls:
            tool_call = output.tool_calls[0]
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            tool_result = await self.session.call_tool(tool_name, tool_args)

            state.result = tool_result.content[0].text 
            state.tryout = 1 if state.tryout is None else state.tryout + 1
        
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nTHE RESULT IS:", state.result)

        return state


    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()




    async def __call__(self, state: MailRoomState):
        """Run the client with the provided state"""
        
        try:
            # # print(f"The tool path:{"ai_mailroom/node2_tool/mcpserver.py"}")
        
            await self.connect_to_server("mcpserver.py")
            # print("Connected to MCP server successfully!")
            await  self.process_query(state) 
            # await self.chat_loop()
            # print("that's all folks!")
        
        finally:
            await self.cleanup()
        print(state.result)
        return state



if __name__ == "__main__":
    # Example usage

    state = MailRoomState(user_input="How many big packages does the mailroom have?")
    client = MCPClient()
    asyncio.run(client(state))