from langgraph.prebuilt import create_react_agent

def create_general_agent(llm):
    return create_react_agent(llm, prompt="You are a helpful assistant. You give answer to user questions based on your knowledge.", tools=[])


