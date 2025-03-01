import streamlit as st
from state import UserState
from langgraph_workflow import workflow_manager

def main():
    st.title("Welcome to the Toyota Assistant!")
    st.write("Ask about vehicle availability, book service appointments, or schedule test drives.")
    
    # Text input for the user query
    user_input = st.text_input("Your Query", "")
    
    if user_input:
        # Create a UserState from the input query
        state = UserState(user_query=user_input)
        try:
            result = workflow_manager.run(state)
            # If result is returned as a dict-like object, convert it to UserState
            if isinstance(result, dict):
                result = UserState(**result)
            st.subheader("Assistant Response")
            st.write(result.final_response)
        except Exception as e:
            st.error(f"Error processing request: {e}")

if __name__ == "__main__":
    main()
