"""
vehicle_availability.py - Vehicle Availability Workflow
Defines VehicleAvailabilityWorkflow which checks Toyota inventory.
"""
from copy import deepcopy
from state import UserState

class VehicleAvailabilityWorkflow:
    def __init__(self):
        # Sample inventory: at least 10 vehicles with model, year, and location.
        self.inventory = [
            {"model": "Camry", "year": 2023, "location": "New York"},
            {"model": "Corolla", "year": 2022, "location": "Los Angeles"},
            {"model": "RAV4", "year": 2023, "location": "Chicago"},
            {"model": "Highlander", "year": 2023, "location": "Houston"},
            {"model": "Prius", "year": 2021, "location": "San Francisco"},
            {"model": "Tacoma", "year": 2022, "location": "Phoenix"},
            {"model": "Tundra", "year": 2023, "location": "Philadelphia"},
            {"model": "4Runner", "year": 2023, "location": "San Antonio"},
            {"model": "Sequoia", "year": 2022, "location": "San Diego"},
            {"model": "Sienna", "year": 2023, "location": "Dallas"},
            {"model": "Yaris", "year": 2021, "location": "Miami"},
            {"model": "Avalon", "year": 2022, "location": "Seattle"},
            {"model": "C-HR", "year": 2023, "location": "Boston"},
            {"model": "Supra", "year": 2023, "location": "Detroit"},
            {"model": "Land Cruiser", "year": 2023, "location": "Atlanta"}
        ]


    def process(self, state: UserState) -> UserState:
        """Checks inventory for vehicles matching the user's query."""
        new_state = deepcopy(state)
        query = state.user_query.lower()
        matching = [v for v in self.inventory if v["model"].lower() in query]
        if matching:
            response_lines = [f"{v['model']} {v['year']} - {v['location']}" for v in matching]
            new_state.retrieved_data = "\n".join(response_lines)
        else:
            new_state.retrieved_data = "No vehicles found matching your query."
        return new_state

# For LangGraph integration, expose an instance method:
vehicle_availability = VehicleAvailabilityWorkflow().process
