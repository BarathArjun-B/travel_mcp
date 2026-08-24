import sqlite3
import os
import contextlib
import logging

logger = logging.getLogger(__name__)

# Configurable database path
DB_PATH = os.environ.get("FLIGHT_MCP_DB_PATH", "data/flightmcp.db")

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_dir()

    def _ensure_dir(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)

    @contextlib.contextmanager
    def get_connection(self):
        """Context manager that yields a sqlite3 connection.
        Row factory is set to sqlite3.Row for dict-like access.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize_tables(self):
        """Creates the flights and bookings tables if they don't exist."""
        logger.info(f"Initializing database at {self.db_path}")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create flights table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                airline TEXT NOT NULL,
                flight_number TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                price INTEGER NOT NULL,
                currency TEXT NOT NULL,
                available_seats INTEGER NOT NULL,
                aircraft TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """)

            # Create bookings table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_reference TEXT NOT NULL UNIQUE,
                flight_id INTEGER NOT NULL,
                passenger_name TEXT NOT NULL,
                passenger_email TEXT NOT NULL,
                passenger_phone TEXT NOT NULL,
                seat_number TEXT,
                total_price INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(flight_id) REFERENCES flights(id)
            )
            """)
        logger.info("Database initialized successfully.")
