from mcp.server import MCPServer
from typing import Optional
from ..database import Database
from ..services.booking_service import BookingService

def register_booking_tools(mcp: MCPServer, db: Database):
    booking_service = BookingService(db)

    @mcp.tool()
    def book_flight(flight_id: int, passenger_name: str, 
                    passenger_email: str, passenger_phone: str, 
                    seat_number: Optional[str] = None) -> dict:
        """Create a simulated flight booking in the local SQLite database. This does NOT purchase a real airline ticket or process payment. Use this ONLY after receiving explicit user confirmation to book."""
        return booking_service.book_flight(
            flight_id, passenger_name, passenger_email, passenger_phone, seat_number
        )

    @mcp.tool()
    def get_booking(booking_reference: str) -> dict:
        """Retrieve a simulated booking by its reference code (e.g. FLM-XXXXXX)."""
        booking = booking_service.get_booking(booking_reference)
        if not booking:
            return {"error": f"Booking {booking_reference} does not exist."}
        return booking.model_dump()

    @mcp.tool()
    def cancel_booking(booking_reference: str) -> dict:
        """Cancel a simulated booking and restore the seat availability."""
        return booking_service.cancel_booking(booking_reference)
