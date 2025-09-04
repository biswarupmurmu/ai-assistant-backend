from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

@tool
def smash_numbers(a: int, b: int) -> str:
    """Smash two numbers"""
    return str(a) + str(b) + " smashed"


def create_smasher_agent(llm):
    return create_react_agent(llm, prompt="Help user smash numbers", tools=[smash_numbers])

