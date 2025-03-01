"""
assistant_core.py - Main entry point for the AI assistant core
Defines AssistantCore, which:
• Receives user queries
• Routes the query to the correct workflow via an LLM-based prompt
• Aggregates workflow results and generates a final answer
"""
from copy import deepcopy
from langchain.schema import SystemMessage, HumanMessage
from llm_config import llm_core, llm_final
from prompts import ROUTING_PROMPT, FINAL_ANSWER_PROMPT
from state import UserState

class AssistantCore:
    def __init__(self):
        pass

    def route_request(self, state: UserState) -> UserState:
        """Routes the user query to the appropriate workflow."""
        new_state = deepcopy(state)
        formatted_prompt = ROUTING_PROMPT.format(query=state.user_query)
        try:
            response = llm_core.invoke([
                SystemMessage(content=formatted_prompt),
                HumanMessage(content=f"User Query: {state.user_query}")
            ])
            workflow_decision = response.content.strip().lower()
            valid_workflows = ["vehicle_availability", "service_booking", "test_drive"]
            if workflow_decision not in valid_workflows:
                print(f"Invalid workflow decision: '{workflow_decision}'. Defaulting to vehicle_availability.")
                workflow_decision = "vehicle_availability"
            new_state.workflow_decision = workflow_decision
            print(f"Routing decision: '{workflow_decision}' for query: '{state.user_query}'")
        except Exception as e:
            print(f"Error in route_request: {e}")
            new_state.workflow_decision = "vehicle_availability"  # Default routing on error
        return new_state

    def generate_answer(self, state: UserState) -> UserState:
        """Generates the final answer from the user query and retrieved data."""
        new_state = deepcopy(state)
        formatted_prompt = FINAL_ANSWER_PROMPT.format(
            query=state.user_query,
            data=state.retrieved_data or "No relevant data found."
        )
        try:
            response = llm_final.invoke([
                SystemMessage(content=formatted_prompt),
                HumanMessage(content=f"User Query: {state.user_query}\nRetrieved Data: {state.retrieved_data}")
            ])
            new_state.final_response = response.content.strip()
            print(f"Generated final response for query: '{state.user_query}'")
        except Exception as e:
            print(f"Error in generate_answer: {e}")
            new_state.final_response = "I'm sorry, I encountered an error generating a response. Please try again."
        return new_state
