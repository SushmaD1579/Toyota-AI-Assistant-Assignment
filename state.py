"""
state.py - Defines the state object passed between nodes
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel

class UserState(BaseModel):
    user_query: str
    workflow_decision: Optional[str] = None
    retrieved_data: Optional[str] = None
    final_response: Optional[str] = None

    def dict_for_llm(self) -> Dict[str, Any]:
        return {
            "user_query": self.user_query,
            "workflow_decision": self.workflow_decision or "Not determined yet",
            "retrieved_data": self.retrieved_data or "No data retrieved yet",
            "final_response": self.final_response or "No response generated yet"
        }
