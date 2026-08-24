# MCP Basics

## What is MCP?
MCP stands for **Model Context Protocol**. It is an open standard that allows AI models like Claude to securely connect to local or remote systems, databases, and APIs.

## Why does MCP exist?
LLMs (Large Language Models) natively only know about the data they were trained on. To make them useful for real-world tasks, they need access to live data and the ability to perform actions. MCP provides a standardized, secure way to give LLMs these capabilities.

## Terminology

### MCP Client
The application hosting the LLM. In this project, the MCP Client is **Claude Desktop**. It is responsible for parsing your natural language, deciding which tools to call, and presenting the results back to you.

### MCP Server
The application providing the data and tools. In this project, our Python application is the **MCP Server**. It connects to the SQLite database and performs the actual business logic.

### Tools
Functions exposed by the MCP Server that the MCP Client can call. Tools have strict schemas (inputs and outputs) and execute on the server. For example, `search_flights` is a tool.

### Resources
Static or dynamic data exposed by the MCP Server that the Client can read to gain context, similar to reading a file. (Not heavily used in Phase 1 of this project).

## How does Claude call a tool?
1. You say: "Find flights from Chennai to Delhi."
2. Claude (Client) looks at the list of tools the Server provided and sees `search_flights`.
3. Claude sends a JSON-RPC message over the MCP protocol to the Server, calling `search_flights` with the requested origin and destination.
4. The Server executes the Python function, queries SQLite, and returns the result as JSON.
5. Claude reads the JSON and formats a natural language response for you.
