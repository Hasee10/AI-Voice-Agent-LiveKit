import sqlite3
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class Car:
    vin: str
    make: str
    model: str
    year: int

class Database:
    def __init__(self, db_path: str = "cars.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cars (
                    vin TEXT PRIMARY KEY,
                    make TEXT,
                    model TEXT,
                    year INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vin TEXT,
                    date TEXT,
                    time TEXT,
                    service_type TEXT,
                    FOREIGN KEY(vin) REFERENCES cars(vin)
                )
            ''')
            conn.commit()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    # --- Car Functions ---
    def create_car(self, vin: str, make: str, model: str, year: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO cars (vin, make, model, year) VALUES (?, ?, ?, ?)',
                    (vin, make, model, year)
                )
                conn.commit()
                return f"Car created successfully: {year} {make} {model} ({vin})"
            except sqlite3.IntegrityError:
                return "Error: A car with this VIN already exists."

    def get_car_by_vin(self, vin: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT vin, make, model, year FROM cars WHERE vin = ?', (vin,))
            row = cursor.fetchone()
            if row:
                return f"Found Car: {row[3]} {row[1]} {row[2]}"
            return "Car not found."

    # --- ADVANCED Appointment Functions ---

    def is_slot_available(self, date: str, time: str):
        """Checks if a slot is already taken by ANYONE."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM appointments WHERE date = ? AND time = ?', (date, time))
            return cursor.fetchone() is None

    def create_appointment(self, vin: str, date: str, time: str, service_type: str = "General Service"):
        if not self.is_slot_available(date, time):
            return f"Error: The slot on {date} at {time} is already taken. Please choose another time."

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO appointments (vin, date, time, service_type) VALUES (?, ?, ?, ?)',
                (vin, date, time, service_type)
            )
            conn.commit()
            return f"Success! Appointment booked for {date} at {time}."

    def cancel_appointment(self, vin: str, date: str, time: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM appointments WHERE vin = ? AND date = ? AND time = ?',
                (vin, date, time)
            )
            if cursor.rowcount > 0:
                conn.commit()
                return f"Appointment on {date} at {time} has been cancelled."
            return "Error: No appointment found matching those details."

    def reschedule_appointment(self, vin: str, old_date: str, old_time: str, new_date: str, new_time: str):
        # 1. Check if new slot is free
        if not self.is_slot_available(new_date, new_time):
            return f"Error: The new slot on {new_date} at {new_time} is unavailable."

        # 2. Update the record
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE appointments SET date = ?, time = ? WHERE vin = ? AND date = ? AND time = ?',
                (new_date, new_time, vin, old_date, old_time)
            )
            if cursor.rowcount > 0:
                conn.commit()
                return f"Rescheduled successfully from {old_date} {old_time} to {new_date} {new_time}."
            return "Error: Could not find the original appointment to reschedule."