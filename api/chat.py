from fastapi import APIRouter, Request
from pydantic import BaseModel
from langchain_core.messages import HumanMessage


chat = APIRouter()

class ChatModel(BaseModel):
    thread_id : str
    prompt : str

@chat.get("/")
async def get_chat():
    return {"message" : "Hello from chat router"}

@chat.post("/")
async def chat_response(data : ChatModel, request: Request):
    thread_id = data.thread_id
    prompt = data.prompt
    config={"configurable" : {"thread_id" : thread_id}}
    workflow = request.app.state.workflow
    try:
        response = await workflow.ainvoke({"messages": [HumanMessage(content=prompt)]}, config=config)
        return {"message" : response['messages'][-1].content}
    except:
        return {"message" : "Sorry, I cannot process your request now. :("}
