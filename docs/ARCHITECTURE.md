# Architecture

This document explains the complete request flow in the FLIGHT MCP system.

## The Stack
- **Client:** Claude Desktop (acting as the MCP Client)
- **Protocol:** MCP (JSON-RPC over stdio)
- **Server:** Python 3.11+ using `mcp.server.fastmcp.FastMCP`
- **Database:** SQLite local file (`data/flightmcp.db`)

## Request Flow Example

**User:** "I need a flight from Chennai to Delhi tomorrow at 6 PM."

↓

**Claude Desktop (MCP Client)**
Understands the user request and determines that it needs flight data. It decides to use the `search_flights` tool.

↓

**MCP Protocol**
Claude sends a structured call over stdio:
```json
{
  "method": "tools/call",
  "params": {
    "name": "search_flights",
    "arguments": {
      "origin": "Chennai",
      "destination": "Delhi",
      "date": "2026-09-05",
      "preferred_time": "18:00"
    }
  }
}
```

↓

**Flight MCP Server (Python)**
Receives the request and routes it to the `search_flights` Python function in `src/flight_mcp/tools/flight_tools.py`.

↓

**Flight Service (Business Logic)**
Constructs a safe SQL query using parameter binding to prevent SQL injection.

↓

**SQLite Database**
Executes the query and returns matching rows.

↓

**Flight Service -> MCP Server**
The rows are mapped to Pydantic objects (`Flight`), converted to dicts, and returned over MCP.

↓

**Claude Desktop**
Receives the structured data, formats it beautifully in markdown, and presents it to the user.

## Booking Request Flow (Human-in-the-Loop)

**User:** "I want to book the IndiGo flight."

↓

**Claude Desktop**
Collects passenger info.

↓

**Claude Desktop**
Presents a Final Booking Summary and asks: "Do you want me to confirm this booking?"

↓

**User:** "Yes, confirm."

↓

**Claude Desktop -> MCP Protocol -> MCP Server**
Calls `book_flight` tool.

↓

**Booking Service**
Begins a transaction:
1. Verifies the flight exists and is scheduled.
2. Verifies `available_seats > 0`.
3. Decrements `available_seats`.
4. Inserts a new booking row with a unique `booking_reference`.
5. Commits transaction.

↓

**Claude Desktop**
Receives the booking reference and tells the user: "Booking confirmed. Reference: FLM-XXXXXX".
