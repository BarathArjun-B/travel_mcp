from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Flight(BaseModel):
    id: int
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    price: int
    currency: str
    available_seats: int
    aircraft: str
    status: str

class Booking(BaseModel):
    id: int
    booking_reference: str
    flight_id: int
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    seat_number: Optional[str] = None
    total_price: int
    status: str
    created_at: str

class BookingSummary(BaseModel):
    booking_reference: str
    status: str
    passenger_name: str
    flight: dict

class SearchFlightsRequest(BaseModel):
    origin: str
    destination: str
    date: str
    preferred_time: Optional[str] = None
    max_price: Optional[int] = None
    airline: Optional[str] = None

class BookFlightRequest(BaseModel):
    flight_id: int
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    seat_number: Optional[str] = None
