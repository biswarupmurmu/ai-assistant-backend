from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_openai import ChatOpenAI

from workflow.test_agent import create_test_agent

llm = ChatOpenAI(model = "gpt-4o-mini")

test_agent = create_test_agent(llm=llm)

graph = StateGraph(MessagesState)

graph.add_node("test_agent", test_agent)

graph.add_edge(START, "test_agent")
graph.add_edge("test_agent", END)

if __name__ == "__main__":
    pass
