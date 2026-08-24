import pytest
import tempfile
import os
from flight_mcp.database import Database
from flight_mcp.services.booking_service import BookingService
from flight_mcp.services.flight_service import FlightService

@pytest.fixture
def booking_service():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    db = Database(path)
    db.initialize_tables()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO flights (airline, flight_number, origin, destination, departure_time, arrival_time, price, currency, available_seats, aircraft, status)
        VALUES 
        ('IndiGo', '6E123', 'Chennai', 'Delhi', '2026-09-05T18:15:00', '2026-09-05T21:05:00', 5200, 'INR', 1, 'Airbus A320', 'scheduled'),
        ('Air India', 'AI456', 'Chennai', 'Delhi', '2026-09-05T19:00:00', '2026-09-05T21:50:00', 5600, 'INR', 0, 'Airbus A320neo', 'scheduled')
        """)
        
    yield BookingService(db)
    os.remove(path)

def test_book_flight_success(booking_service):
    res = booking_service.book_flight(1, "Test User", "test@test.com", "9999999999")
    assert "error" not in res
    assert res["status"] == "CONFIRMED"
    assert "booking_reference" in res
    
    # Check seats decreased
    flight_service = FlightService(booking_service.db)
    seats_res = flight_service.check_seats(1)
    assert seats_res["available_seats"] == 0

def test_book_flight_full(booking_service):
    res = booking_service.book_flight(2, "Test User", "test@test.com", "9999999999")
    assert "error" in res
    assert res["error"] == "Flight 2 is fully booked."

def test_book_flight_invalid(booking_service):
    res = booking_service.book_flight(999, "Test User", "test@test.com", "9999999999")
    assert "error" in res

def test_get_booking(booking_service):
    res = booking_service.book_flight(1, "Test User", "test@test.com", "9999999999")
    ref = res["booking_reference"]
    
    booking = booking_service.get_booking(ref)
    assert booking is not None
    assert booking.passenger_name == "Test User"
    assert booking.flight["flight_number"] == "6E123"

def test_get_booking_invalid(booking_service):
    booking = booking_service.get_booking("INVALID")
    assert booking is None

def test_cancel_booking(booking_service):
    res = booking_service.book_flight(1, "Test User", "test@test.com", "9999999999")
    ref = res["booking_reference"]
    
    # Cancel it
    cancel_res = booking_service.cancel_booking(ref)
    assert "error" not in cancel_res
    assert cancel_res["status"] == "CANCELLED"
    
    # Verify seat restored
    flight_service = FlightService(booking_service.db)
    seats_res = flight_service.check_seats(1)
    assert seats_res["available_seats"] == 1
    
    # Verify booking status
    booking = booking_service.get_booking(ref)
    assert booking.status == "CANCELLED"

def test_cancel_already_cancelled(booking_service):
    res = booking_service.book_flight(1, "Test User", "test@test.com", "9999999999")
    ref = res["booking_reference"]
    booking_service.cancel_booking(ref)
    
    # Second cancellation
    cancel_res2 = booking_service.cancel_booking(ref)
    assert "error" in cancel_res2
