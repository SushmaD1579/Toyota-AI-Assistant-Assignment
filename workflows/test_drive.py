# """
# test_drive.py - Test Drive Scheduling Workflow
# Defines TestDriveWorkflow which schedules a test drive at a Toyota dealership.
# """
# from copy import deepcopy
# from state import UserState

# class TestDriveWorkflow:
#     def __init__(self):
#         # Hardcoded list of dealerships with available test drive slots
#         self.dealerships = {
#             "new york": ["09:00", "10:00", "14:00", "16:00"],
#             "los angeles": ["09:30", "11:00", "13:00", "15:00"],
#             "chicago": ["10:00", "11:00", "13:00", "15:00"],
#             "houston": ["08:30", "10:30", "12:30", "14:30"],
#             "phoenix": ["09:00", "12:00", "15:00"],
#             "philadelphia": ["08:00", "10:00", "13:00", "16:00"],
#             "san antonio": ["09:30", "11:30", "14:30"],
#             "san diego": ["08:45", "11:15", "14:45"],
#             "dallas": ["09:00", "11:00", "13:30", "15:30"],
#             "san jose": ["10:00", "12:00", "14:00"]
#         }

#     def process(self, state: UserState) -> UserState:
#         """Schedules a test drive by matching the query to a dealership."""
#         new_state = deepcopy(state)
#         query = state.user_query.lower()
#         found = False
#         for dealership, slots in self.dealerships.items():
#             if dealership in query:
#                 new_state.retrieved_data = f"Available test drive slots at {dealership.title()}: {', '.join(slots)}"
#                 found = True
#                 break
#         if not found:
#             available = ", ".join([d.title() for d in self.dealerships.keys()])
#             new_state.retrieved_data = f"No dealership specified. Available dealerships: {available}"
#         return new_state

# # Expose an instance method for LangGraph integration:
# test_drive = TestDriveWorkflow().process

"""
test_drive.py - Test Drive Scheduling Workflow
Defines TestDriveWorkflow which schedules a test drive at a Toyota dealership.
"""
from copy import deepcopy
from state import UserState

class TestDriveWorkflow:
    def __init__(self):
        # Hardcoded list of dealerships with available test drive slots (list of dictionaries)
        self.dealerships = [
            {"city": "New York", "slots": ["10:00", "14:00"]},
            {"city": "Los Angeles", "slots": ["09:00", "13:00"]},
            {"city": "Chicago", "slots": ["11:00", "15:00"]},
            {"city": "Houston", "slots": ["08:30", "12:00", "16:00"]},
            {"city": "Phoenix", "slots": ["09:30", "13:30"]},
            {"city": "Philadelphia", "slots": ["10:00", "14:00"]},
            {"city": "San Antonio", "slots": ["09:00", "11:00", "15:00"]},
            {"city": "San Diego", "slots": ["08:45", "12:15", "16:15"]},
            {"city": "Dallas", "slots": ["09:15", "13:15"]},
            {"city": "San Jose", "slots": ["10:30", "14:30"]}
        ]

    def process(self, state: UserState) -> UserState:
        """Schedules a test drive by matching the query to a dealership in the list."""
        new_state = deepcopy(state)
        query = state.user_query.lower()
        matching_dealerships = [
            dealership for dealership in self.dealerships
            if dealership["city"].lower() in query
        ]
        if matching_dealerships:
            # Use the first matching dealership for the response
            dealership = matching_dealerships[0]
            new_state.retrieved_data = (
                f"Available test drive slots in {dealership['city']}: "
                + ", ".join(dealership["slots"])
            )
        else:
            # If no match found, list available dealership cities
            available_cities = ", ".join([d["city"] for d in self.dealerships])
            new_state.retrieved_data = (
                "No specific dealership found in your query. "
                f"Available cities: {available_cities}"
            )
        return new_state

# Expose an instance method for LangGraph integration:
test_drive = TestDriveWorkflow().process
