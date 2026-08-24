from mcp.server import MCPServer
import logging
import sys

from .database import Database
from .tools.flight_tools import register_flight_tools
from .tools.booking_tools import register_booking_tools

# Configure basic logging to stderr so it doesn't interfere with stdio MCP transport
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stderr)
logger = logging.getLogger(__name__)

# Initialize database and MCPServer server
db = Database()
mcp = MCPServer("Flight MCP")

# Register tools
register_flight_tools(mcp, db)
register_booking_tools(mcp, db)

def main():
    logger.info("Starting Flight MCP Server")
    db.initialize_tables()
    mcp.run()

if __name__ == "__main__":
    main()
