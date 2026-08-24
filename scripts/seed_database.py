import sys
import os

# Add src to Python path so we can import flight_mcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from flight_mcp.database import Database

def seed_database():
    db = Database()
    db.initialize_tables()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check if we already have flights
        cursor.execute("SELECT COUNT(*) as count FROM flights")
        row = cursor.fetchone()
        
        if row['count'] > 0:
            print("Database already contains flight data. Seed script aborted.")
            return

        sample_flights = [
            # Chennai to Delhi
            ("IndiGo", "6E123", "Chennai", "Delhi", "2026-09-05T18:15:00", "2026-09-05T21:05:00", 5200, "INR", 25, "Airbus A320", "scheduled"),
            ("Air India", "AI456", "Chennai", "Delhi", "2026-09-05T19:00:00", "2026-09-05T21:50:00", 5600, "INR", 15, "Airbus A320neo", "scheduled"),
            ("Akasa Air", "QP789", "Chennai", "Delhi", "2026-09-05T17:30:00", "2026-09-05T20:20:00", 4900, "INR", 40, "Boeing 737 MAX", "scheduled"),
            
            # Chennai to Mumbai
            ("IndiGo", "6E456", "Chennai", "Mumbai", "2026-09-06T10:00:00", "2026-09-06T12:00:00", 4500, "INR", 10, "Airbus A320", "scheduled"),
            ("Vistara", "UK112", "Chennai", "Mumbai", "2026-09-06T14:30:00", "2026-09-06T16:30:00", 6200, "INR", 0, "Airbus A320neo", "scheduled"), # Full flight
            
            # Bangalore to Delhi
            ("Air India", "AI101", "Bangalore", "Delhi", "2026-09-05T08:00:00", "2026-09-05T10:45:00", 7000, "INR", 50, "Boeing 777", "scheduled"),
            
            # Mumbai to Delhi
            ("IndiGo", "6E999", "Mumbai", "Delhi", "2026-09-07T09:00:00", "2026-09-07T11:15:00", 4800, "INR", 30, "Airbus A320", "scheduled"),
            ("SpiceJet", "SG333", "Mumbai", "Delhi", "2026-09-07T18:00:00", "2026-09-07T20:15:00", 4200, "INR", 5, "Boeing 737", "scheduled"),
        ]

        cursor.executemany("""
        INSERT INTO flights (airline, flight_number, origin, destination, departure_time, arrival_time, price, currency, available_seats, aircraft, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_flights)
        
        print(f"Inserted {len(sample_flights)} sample flights.")

if __name__ == "__main__":
    seed_database()
