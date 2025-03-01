"""
langgraph_workflow.py - Defines the LangGraph workflow structure
Contains WorkflowManager that connects the core assistant and specialized workflows.
"""
from langgraph.graph import StateGraph, END
from state import UserState
from assistant_core import AssistantCore
from workflows.vehicle_availability import vehicle_availability
from workflows.service_booking import service_booking
from workflows.test_drive import test_drive

class WorkflowManager:
    def __init__(self):
        self.assistant_core = AssistantCore()
        self.graph = StateGraph(UserState)
        self.setup_graph()

    def setup_graph(self):
        # Add core nodes
        self.graph.add_node("route_request", self.assistant_core.route_request)
        self.graph.add_node("generate_answer", self.assistant_core.generate_answer)
        
        # Add specialized workflow nodes
        self.graph.add_node("vehicle_availability", vehicle_availability)
        self.graph.add_node("service_booking", service_booking)
        self.graph.add_node("test_drive", test_drive)
        
        # Conditional routing: decide which specialized workflow to invoke
        def router(state: UserState):
            decision = state.workflow_decision
            valid = ["vehicle_availability", "service_booking", "test_drive"]
            return decision if decision in valid else "vehicle_availability"
        
        self.graph.add_conditional_edges("route_request", router, {
            "vehicle_availability": "vehicle_availability",
            "service_booking": "service_booking",
            "test_drive": "test_drive"
        })
        
        # Connect specialized workflows to final answer generation
        self.graph.add_edge("vehicle_availability", "generate_answer")
        self.graph.add_edge("service_booking", "generate_answer")
        self.graph.add_edge("test_drive", "generate_answer")
        
        # Set entry point and termination edge
        self.graph.set_entry_point("route_request")
        self.graph.add_edge("generate_answer", END)
    
    def run(self, state: UserState) -> UserState:
        """Runs the workflow with the given user state."""
        compiled = self.graph.compile()
        return compiled.invoke(state)

# For convenience, expose an instance:
workflow_manager = WorkflowManager()
