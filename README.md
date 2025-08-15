# AImaster

<!-- When the class cannot be import from root path to subpath, execute these two line on terminal at Root directory

go to Preference open workspace setting JSON and type: 

{
    "terminal.integrated.env.osx": {
        "PYTHONPATH": "${workspaceFolder}"
    }

    It makes Python able to find and import your project’s modules from anywhere in your workspace when using the VS Code terminal on macOS.
}
-->


<!-- to create a new Venv with UV in new project 
    1. 
    2.   
    3.  
 -->


AI End-to-End Mailroom System

An agentic AI-driven mailroom automation platform integrating LLM reasoning, StateGraph orchestration, MCP client/agent communication, tool calling, and a MySQL database — seamlessly passing processed orders to a hardware control system for execution.

This project demonstrates a full pipeline from natural language task intake → intelligent parsing → database storage → decision-making → hardware dispatch.


🚀 Features

LLM-Powered Processing
Uses Large Language Models for natural language understanding, intent detection, and order parsing.

StateGraph Workflow Orchestration
Encapsulates mailroom logic into a graph-based state machine for predictable, maintainable flows.

MCP Client/Agent Communication
Handles multi-step, context-aware communication between AI agents and connected hardware controllers.

Tool Calling & Function Execution
Dynamically triggers custom tools (database operations, validation, hardware commands) from LLM outputs.

MySQL Integration
Stores and retrieves structured order data for persistence and auditability.

Hardware Dispatch Layer
Passes validated instructions to the physical mailroom hardware system for execution.

End-to-End Automation
From receiving requests → AI decision-making → final physical action.
