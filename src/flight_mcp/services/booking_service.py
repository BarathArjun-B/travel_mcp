from typing import Optional, Dict, Any
import uuid
import datetime
from ..database import Database
from ..models import Booking, BookingSummary
from .flight_service import FlightService

class BookingService:
    def __init__(self, db: Database):
        self.db = db
        self.flight_service = FlightService(db)

    def _generate_booking_reference(self) -> str:
        """Generates a unique booking reference like FLM-XXXXXX"""
        short_uuid = str(uuid.uuid4()).split('-')[0].upper()
        return f"FLM-{short_uuid}"

    def book_flight(self, flight_id: int, passenger_name: str, 
                    passenger_email: str, passenger_phone: str, 
                    seat_number: Optional[str] = None) -> Dict[str, Any]:
        """Creates a simulated booking for a flight in an atomic transaction."""
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Step 1: Check if flight exists and is available, locking the row implicitly in SQLite
            # Actually, SQLite doesn't do row-level locking but we can at least check
            cursor.execute("SELECT * FROM flights WHERE id = ?", (flight_id,))
            row = cursor.fetchone()
            if not row:
                return {"error": f"Flight {flight_id} does not exist."}
            
            available_seats = row['available_seats']
            status = row['status']
            total_price = row['price']
            
            if status != 'scheduled':
                return {"error": f"Flight {flight_id} is not scheduled."}
                
            if available_seats <= 0:
                return {"error": f"Flight {flight_id} is fully booked."}
                
            # Step 2: Decrease available seats
            cursor.execute("UPDATE flights SET available_seats = available_seats - 1 WHERE id = ?", (flight_id,))
            
            # Step 3: Insert booking
            booking_ref = self._generate_booking_reference()
            created_at = datetime.datetime.now().isoformat()
            booking_status = "CONFIRMED"
            
            cursor.execute("""
            INSERT INTO bookings (booking_reference, flight_id, passenger_name, passenger_email, passenger_phone, seat_number, total_price, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (booking_ref, flight_id, passenger_name, passenger_email, passenger_phone, seat_number, total_price, booking_status, created_at))
            
            # The transaction commits automatically due to context manager
            
            return {
                "booking_reference": booking_ref,
                "status": booking_status,
                "flight_number": row['flight_number'],
                "passenger_name": passenger_name,
                "total_price": total_price,
                "currency": row['currency']
            }

    def get_booking(self, booking_reference: str) -> Optional[BookingSummary]:
        """Retrieves booking details."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT b.*, f.airline, f.flight_number, f.origin, f.destination
            FROM bookings b
            JOIN flights f ON b.flight_id = f.id
            WHERE b.booking_reference = ?
            """, (booking_reference,))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            return BookingSummary(
                booking_reference=row['booking_reference'],
                status=row['status'],
                passenger_name=row['passenger_name'],
                flight={
                    "airline": row['airline'],
                    "flight_number": row['flight_number'],
                    "origin": row['origin'],
                    "destination": row['destination']
                }
            )

    def cancel_booking(self, booking_reference: str) -> Dict[str, Any]:
        """Cancels a booking and restores a seat."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM bookings WHERE booking_reference = ?", (booking_reference,))
            row = cursor.fetchone()
            
            if not row:
                return {"error": f"Booking {booking_reference} does not exist."}
                
            if row['status'] == 'CANCELLED':
                return {"error": f"Booking {booking_reference} is already cancelled."}
                
            flight_id = row['flight_id']
            
            # Update status
            cursor.execute("UPDATE bookings SET status = 'CANCELLED' WHERE booking_reference = ?", (booking_reference,))
            
            # Restore seat
            cursor.execute("UPDATE flights SET available_seats = available_seats + 1 WHERE id = ?", (flight_id,))
            
            return {
                "booking_reference": booking_reference,
                "status": "CANCELLED",
                "message": "Cancellation confirmed. Seat restored."
            }
