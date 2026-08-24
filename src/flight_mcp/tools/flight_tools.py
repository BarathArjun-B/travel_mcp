from mcp.server import MCPServer
from typing import Optional
from ..database import Database
from ..services.flight_service import FlightService

def register_flight_tools(mcp: MCPServer, db: Database):
    flight_service = FlightService(db)

    @mcp.tool()
    def search_flights(origin: str, destination: str, date: str, 
                       preferred_time: Optional[str] = None, 
                       max_price: Optional[int] = None, 
                       airline: Optional[str] = None) -> list[dict]:
        """Search the local sample flight inventory. This tool returns fictional/demo flight options and is not connected to live airline availability."""
        flights = flight_service.search_flights(
            origin, destination, date, preferred_time, max_price, airline
        )
        return [f.model_dump() for f in flights]

    @mcp.tool()
    def get_flight(flight_id: int) -> dict:
        """Retrieve complete information for one fictional flight by its ID."""
        flight = flight_service.get_flight(flight_id)
        if not flight:
            return {"error": f"Flight {flight_id} does not exist."}
        return flight.model_dump()

    @mcp.tool()
    def check_seats(flight_id: int) -> dict:
        """Check currently available seats for a demo flight."""
        return flight_service.check_seats(flight_id)
