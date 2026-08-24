import pytest
import sqlite3
import tempfile
import os
from flight_mcp.database import Database

@pytest.fixture
def memory_db():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    db = Database(path)
    db.initialize_tables()
    yield db
    os.remove(path)

def test_database_initialization(memory_db):
    with memory_db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check flights table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='flights'")
        assert cursor.fetchone() is not None
        
        # Check bookings table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'")
        assert cursor.fetchone() is not None
