from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from workflow.smasher_agent import create_smasher_agent
from workflow.general_agent import create_general_agent

#llm = ChatOpenAI(model = "gpt-4o-mini")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    #temperature=0.10,
)

smasher_agent = create_smasher_agent(llm=llm)
general_agent = create_general_agent(llm=llm)


def router(state: MessagesState):
    user_prompt = state['messages'][-1].content
    system_role = '''
        You are a router. Your task is route the task/prompt to the best possible agent based on the context.
        Observe the current conversation very carefully, based on that only you route to appropriate agent.
        - 'smash' if it's something about Smashing numbers.
        - 'general' if it's something else and the LLM should answer directly.

        Reply with ONLY: 'smash' or 'general'.
    '''

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_role),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]
    )

    chain = prompt | llm

    llm_response = chain.invoke({"input" : user_prompt, "chat_history" : state["messages"]})

    decision = llm_response.content.strip().lower()

    if decision == "smash":
        return "smash"
    else:
        return "general"


graph = StateGraph(MessagesState)

graph.add_node("smasher_agent", smasher_agent)
graph.add_node("general_agent", general_agent)

graph.add_edge("general_agent", END)
graph.add_conditional_edges(START, router, {
    "smash": "smasher_agent",
    "general": "general_agent"
})
graph.add_edge("smasher_agent", END)
graph.add_edge("general_agent", END)

if __name__ == "__main__":
    pass
