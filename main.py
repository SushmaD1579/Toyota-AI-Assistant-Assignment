from state import UserState
from langgraph_workflow import workflow_manager

def run_assistant():
    print("\n" + "="*50)
    print("Welcome to the Toyota Assistant!")
    print("You can ask about vehicle availability, book service appointments, or schedule test drives.")
    print("Type 'exit' to quit.")
    print("="*50 + "\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Thank you for using the Toyota Assistant. Goodbye!")
            break
        
        # Initialize state with user query
        state = UserState(user_query=user_input)
        
        # Process through the workflow graph
        try:
            result = workflow_manager.run(state)
            # Convert result back into a UserState if necessary
            if isinstance(result, dict):
                result = UserState(**result)
            if result.final_response:
                print("Assistant:", result.final_response)
            else:
                print("Assistant: I'm sorry, I couldn't generate a proper response.")
        except Exception as e:
            print(f"Error: {e}")
            print("Assistant: I encountered an error processing your request. Please try again.")
        
        print()

if __name__ == "__main__":
    run_assistant()
