import logging
from livekit.agents import function_tool, RunContext
from database import Database

logger = logging.getLogger("voice-agent")
db = Database()

# Global state
class SessionState:
    def __init__(self):
        self.current_vin = None

state = SessionState()

@function_tool
async def lookup_car(ctx: RunContext, vin: str):
    """Lookup a car by its VIN."""
    logger.info(f"Looking up car with VIN: {vin}")
    result = db.get_car_by_vin(vin)
    if "Found Car" in result:
        state.current_vin = vin
        return f"{result}. (Vehicle Identified)"
    return result

@function_tool
async def create_car(ctx: RunContext, vin: str, make: str, model: str, year: int):
    """Create a new car profile."""
    logger.info(f"Creating car: {vin} {make} {model} {year}")
    result = db.create_car(vin, make, model, year)
    if "created successfully" in result:
        state.current_vin = vin
    return result

@function_tool
async def has_selected_car(ctx: RunContext):
    """Check if vehicle is identified."""
    if state.current_vin:
        return f"True. Current VIN: {state.current_vin}"
    return "False. No vehicle selected."

# --- BOOKING TOOLS ---

@function_tool
async def book_appointment(ctx: RunContext, date: str, time: str):
    """Book a service appointment."""
    if not state.current_vin:
        return "Error: Ask for VIN first."
    return db.create_appointment(state.current_vin, date, time)

@function_tool
async def cancel_appointment(ctx: RunContext, date: str, time: str):
    """
    Cancel an existing appointment.
    Args:
        date: The date of the appointment to cancel.
        time: The time of the appointment to cancel.
    """
    if not state.current_vin:
        return "Error: Ask for VIN first."
    return db.cancel_appointment(state.current_vin, date, time)

@function_tool
async def reschedule_appointment(ctx: RunContext, old_date: str, old_time: str, new_date: str, new_time: str):
    """
    Reschedule an appointment to a new time.
    Args:
        old_date: The original date.
        old_time: The original time.
        new_date: The NEW desired date.
        new_time: The NEW desired time.
    """
    if not state.current_vin:
        return "Error: Ask for VIN first."
    return db.reschedule_appointment(state.current_vin, old_date, old_time, new_date, new_time)