"""
service_booking.py - Service Appointment Booking Workflow
Defines ServiceBookingWorkflow which simulates booking a service appointment.
"""
from copy import deepcopy
from state import UserState

class ServiceBookingWorkflow:
    def __init__(self):
        # Mock dataset of available appointment slots
        self.appointments = [
            {"date": "2023-10-01", "time": "09:00", "location": "New York"},
            {"date": "2023-10-01", "time": "11:00", "location": "New York"},
            {"date": "2023-10-02", "time": "14:00", "location": "Chicago"},
            {"date": "2023-10-03", "time": "10:00", "location": "Los Angeles"},
            {"date": "2023-10-04", "time": "12:00", "location": "Houston"},
            {"date": "2023-10-05", "time": "09:30", "location": "Phoenix"},
            {"date": "2023-10-06", "time": "15:00", "location": "Philadelphia"},
            {"date": "2023-10-07", "time": "10:30", "location": "San Antonio"},
            {"date": "2023-10-08", "time": "11:30", "location": "San Diego"},
            {"date": "2023-10-09", "time": "14:30", "location": "Dallas"}
        ]

    def process(self, state: UserState) -> UserState:
        """Checks for available appointment slots based on the query."""
        new_state = deepcopy(state)
        query = state.user_query.lower()
        matching_slots = [
            f"{appt['date']} at {appt['time']} - {appt['location']}"
            for appt in self.appointments
            if appt['time'] in query or appt['date'] in query
        ]
        if matching_slots:
            new_state.retrieved_data = "Available slots:\n" + "\n".join(matching_slots)
        else:
            new_state.retrieved_data = "No matching appointment slots found. Please try a different time or date."
        return new_state

# Expose an instance method for LangGraph integration:
service_booking = ServiceBookingWorkflow().process
