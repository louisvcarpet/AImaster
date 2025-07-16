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


    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def call_tool(self, tool_name: str, tool_args: dict):
        pass
    
    async def process_query(self, query: str) -> str:
  
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
        output = await chain.ainvoke({"query", query})


        if output.tool_calls:
            tool_call = output.tool_calls[0]
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            tool_result = await self.session.call_tool(tool_name, tool_args)

        return tool_result.content[0].text


    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    
    if len(sys.argv) < 2:
        print(f"Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    client.process_query(query = state.user_input)
    try:
        print(f"The tool path:{sys.argv[1]}")
        
        await client.connect_to_server(sys.argv[1])
        print("Connected to MCP server successfully!")
        
        await client.chat_loop()
        print("that's all folks!")
      
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())



















#   async def process_query(self, query: str) -> str:
        
#         """Process a query using ChatGPT and available tools"""
#         messages = [
#             {
#                 "role": "user",
#                 "content": query
#             }
#         ]

#         response = await self.session.list_tools()
#         available_tools = [{ 
#             "name": tool.name,
#             "description": tool.description,
#             "input_schema": tool.inputSchema
#         } for tool in response.tools]
      
# ###############################################################
#         llm = LLMBase()

#         # Initial Claude API call
#         response = await llm.ainvoke(query)
# ###############################################################
#         # Process response and handle tool calls
#         tool_results = []
#         final_text = []

#         for content in response.content:
#             if content.type == 'text':
#                 final_text.append(content.text)
#             elif content.type == 'tool_use':
#                 tool_name = content.name
#                 tool_args = content.input

#                 # Execute tool call
#                 result = await self.session.call_tool(tool_name, tool_args)
#                 tool_results.append({"call": tool_name, "result": result})
#                 final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

#                 # Continue conversation with tool results
#                 if hasattr(content, 'text') and content.text:
#                     messages.append({
#                     "role": "assistant",
#                     "content": content.text
#                     })
#                 messages.append({
#                     "role": "user", 
#                     "content": result.content
#                 })

#                 # Get next response from Claude
#                 response = self.anthropic.messages.create(
#                     model="claude-3-5-sonnet-20241022",
#                     max_tokens=1000,
#                     messages=messages,
#                 )

#                 final_text.append(response.content[0].text)

#         return "\n".join(final_text)