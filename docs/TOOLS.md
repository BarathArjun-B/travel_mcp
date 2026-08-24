# MCP Tools

This document outlines the tools exposed by the FLIGHT MCP server.

## 1. search_flights
**Purpose:** Search the local sample flight inventory. This tool returns fictional/demo flight options and is not connected to live airline availability.
**Inputs:**
- `origin` (string, required)
- `destination` (string, required)
- `date` (string, required) - ISO date (YYYY-MM-DD)
- `preferred_time` (string, optional)
- `max_price` (integer, optional)
- `airline` (string, optional)

## 2. get_flight
**Purpose:** Retrieve complete information for one fictional flight by its ID.
**Inputs:**
- `flight_id` (integer, required)

## 3. check_seats
**Purpose:** Check currently available seats for a demo flight.
**Inputs:**
- `flight_id` (integer, required)
**Output Example:**
```json
{
  "flight_id": 1,
  "available_seats": 25,
  "status": "available"
}
```

## 4. book_flight
**Purpose:** Create a simulated flight booking in the local SQLite database. This does NOT purchase a real airline ticket or process payment. Use this ONLY after receiving explicit user confirmation to book.
**Inputs:**
- `flight_id` (integer, required)
- `passenger_name` (string, required)
- `passenger_email` (string, required)
- `passenger_phone` (string, required)
- `seat_number` (string, optional)

## 5. get_booking
**Purpose:** Retrieve a simulated booking by its reference code.
**Inputs:**
- `booking_reference` (string, required) - e.g., "FLM-A1B2C3"

## 6. cancel_booking
**Purpose:** Cancel a simulated booking and restore the seat availability.
**Inputs:**
- `booking_reference` (string, required)
