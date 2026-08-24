import pytest
import tempfile
import os
from flight_mcp.database import Database
from flight_mcp.services.flight_service import FlightService

@pytest.fixture
def flight_service():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    db = Database(path)
    db.initialize_tables()
    
    # Insert sample data
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO flights (airline, flight_number, origin, destination, departure_time, arrival_time, price, currency, available_seats, aircraft, status)
        VALUES 
        ('IndiGo', '6E123', 'Chennai', 'Delhi', '2026-09-05T18:15:00', '2026-09-05T21:05:00', 5200, 'INR', 25, 'Airbus A320', 'scheduled'),
        ('Air India', 'AI456', 'Chennai', 'Delhi', '2026-09-05T19:00:00', '2026-09-05T21:50:00', 5600, 'INR', 0, 'Airbus A320neo', 'scheduled')
        """)
        
    yield FlightService(db)
    os.remove(path)

def test_search_flights(flight_service):
    flights = flight_service.search_flights("Chennai", "Delhi", "2026-09-05")
    assert len(flights) == 2
    assert flights[0].flight_number == "6E123"

def test_search_flights_max_price(flight_service):
    flights = flight_service.search_flights("Chennai", "Delhi", "2026-09-05", max_price=5500)
    assert len(flights) == 1
    assert flights[0].price == 5200

def test_search_flights_no_match(flight_service):
    flights = flight_service.search_flights("Chennai", "Mumbai", "2026-09-05")
    assert len(flights) == 0

def test_get_flight_valid(flight_service):
    flight = flight_service.get_flight(1)
    assert flight is not None
    assert flight.flight_number == "6E123"

def test_get_flight_invalid(flight_service):
    flight = flight_service.get_flight(999)
    assert flight is None

def test_check_seats_available(flight_service):
    res = flight_service.check_seats(1)
    assert res['status'] == 'available'
    assert res['available_seats'] == 25

def test_check_seats_full(flight_service):
    res = flight_service.check_seats(2)
    assert res['status'] == 'full'
    assert res['available_seats'] == 0
