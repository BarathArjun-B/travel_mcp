# Claude Desktop Setup

To connect this MCP server to Claude Desktop, you need to update your Claude Desktop configuration file.

## Configuration Path
On Mac, the configuration file is typically located at:
`~/Library/Application Support/Claude/claude_desktop_config.json`

## Configuration Example

Open the configuration file and add the following JSON. 

> **Important:** Replace `<PATH_TO_YOUR_WORKSPACE>` with the actual absolute path to the directory where this project is located (e.g., `/Users/baratharjun/Desktop/medai`).

```json
{
  "mcpServers": {
    "flight-mcp": {
      "command": "uv",
      "args": [
        "run",
        "flight-mcp"
      ],
      "cwd": "<PATH_TO_YOUR_WORKSPACE>"
    }
  }
}
```

### Why `uv run flight-mcp`?
We use `uv run` to ensure that the MCP server is launched using the project's exact virtual environment with all required dependencies (like `mcp` and `pydantic`) loaded correctly. We specify the `cwd` (Current Working Directory) so that the server can correctly find and interact with the `data/flightmcp.db` local SQLite database.

## Testing the Configuration

1. Restart Claude Desktop.
2. Open a new chat in Claude Desktop.
3. Test tool discovery by prompting:
   > "List the flight tools you have available."
4. If successful, Claude should reply detailing `search_flights`, `book_flight`, etc.

Proceed to test the end-to-end booking flow!
