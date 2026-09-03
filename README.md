# ✈️ Flight MCP Server — SQLite Demo

A fully functional **Model Context Protocol (MCP)** demonstration server providing simulated flight search and booking capabilities. 

> [!WARNING]
> **SIMULATION ONLY:** All flights, inventory, and bookings in this system are purely simulated using fictional/sample data. This project **DOES NOT** integrate with any real airline APIs and **DOES NOT** book real flights.

## What is the Project?
This project is a clean, modular Python application designed to teach the fundamentals of the Model Context Protocol (MCP). It acts as a local backend server that seamlessly connects to Claude Desktop, granting the AI safe, controlled access to a local SQLite database for exploring and booking demo flights.

## What is MCP?
The **Model Context Protocol (MCP)** is an open standard that allows AI models (like Claude) to securely connect to local or remote data sources, tools, and services. Instead of the LLM guessing or hallucinating data, MCP allows it to query a deterministic backend system.

## Architecture
The system architecture follows a clean, layered approach:

```text
Claude Desktop (Client)
        ↓ (stdio JSON-RPC)
Python Flight MCP Server
        ↓
Services Layer (Business Logic)
        ↓
SQLite Database (Data Store)
```

## Technology Stack
- **Language:** Python 3.11+
- **Package Manager:** `uv`
- **Framework:** Official MCP Python SDK (`mcp`)
- **Database:** SQLite (local file)
- **Client:** Claude Desktop
---------------------------------------------------------------
## Six Available Tools
The server exposes exactly six robust MCP tools to the AI:

1. `search_flights`: Find available flights by origin, destination, and date.
2. `get_flight`: Retrieve full details and metadata for a specific flight.
3. `check_seats`: Query live seat availability for a flight.
4. `book_flight`: Create a new simulated booking (requires user confirmation).
5. `get_booking`: Retrieve details of an existing booking via a PNR reference.
6. `cancel_booking`: Cancel a booking and restore seat inventory.

## SQLite Demo Database
The system uses a local SQLite database (`data/flightmcp.db`) to store flight inventory and booking states. 
*Note: The actual `.db` file is excluded from version control to prevent stale state issues.*

To initialize the database with fresh demo data, run:
```bash
uv run python scripts/seed_database.py
```

## Installation & Setup
Ensure you have [uv](https://github.com/astral-sh/uv) installed, then sync the dependencies:
```bash
uv sync
```

## Running the Tests
The project includes a robust `pytest` suite for backend verification.
```bash
uv run pytest
```

## Running the MCP Server
To manually verify the server starts correctly (it will block and wait for stdio communication):
```bash
uv run flight-mcp
```
*(Application logs are strictly routed to `stderr` to maintain clean MCP protocol output on `stdout`.)*

## Configuring Claude Desktop
To connect this MCP server to Claude Desktop, edit your Claude Desktop configuration file (typically located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS).

### Claude Desktop Configuration Example:
```json
{
  "mcpServers": {
    "flight-mcp": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--directory",
        "/Users/baratharjun/Desktop/medai",
        "flight-mcp"
      ],
      "cwd": "/Users/baratharjun/Desktop/medai"
    }
  }
}
```
*Note: Adjust the absolute paths to match your local project directory and `uv` installation path.*

## Example Tool Usage
Once connected in Claude Desktop, you can interact naturally:

**User:** "Find me a flight from Chennai to Delhi on 2026-09-05."
*Claude calls `search_flights` and reads the SQLite database.*

**User:** "How many seats are left on flight 1?"
*Claude calls `check_seats`.*

**User:** "I want to book flight 1. My name is Test User, email is test@example.com, phone 9999999999."
*Claude summarizes the request and explicitly asks for confirmation.*

**User:** "Confirmed."
*Claude calls `book_flight` and returns the fictional booking reference (e.g., FLM-XXXXXX).*
