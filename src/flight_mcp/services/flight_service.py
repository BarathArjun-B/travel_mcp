from typing import List, Optional, Dict, Any
from ..database import Database
from ..models import Flight

class FlightService:
    def __init__(self, db: Database):
        self.db = db

    def search_flights(self, origin: str, destination: str, date: str,
                       preferred_time: Optional[str] = None,
                       max_price: Optional[int] = None,
                       airline: Optional[str] = None) -> List[Flight]:
        """Searches for flights based on the given criteria."""
        query = "SELECT * FROM flights WHERE origin = ? AND destination = ? AND date(departure_time) = ?"
        params = [origin, destination, date]

        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
            
        if airline is not None:
            query += " AND airline = ?"
            params.append(airline)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            flights = []
            for row in rows:
                flight = Flight(**dict(row))
                flights.append(flight)
            
            return flights

    def get_flight(self, flight_id: int) -> Optional[Flight]:
        """Retrieves a specific flight by its ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flights WHERE id = ?", (flight_id,))
            row = cursor.fetchone()
            if row:
                return Flight(**dict(row))
            return None

    def check_seats(self, flight_id: int) -> Dict[str, Any]:
        """Checks the available seats for a given flight."""
        flight = self.get_flight(flight_id)
        if not flight:
            return {"error": f"Flight {flight_id} does not exist."}
        
        status = "available" if flight.available_seats > 0 else "full"
        return {
            "flight_id": flight.id,
            "available_seats": flight.available_seats,
            "status": status
        }
