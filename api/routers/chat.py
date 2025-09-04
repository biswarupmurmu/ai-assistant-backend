from fastapi import APIRouter, Request
from langchain_core.messages import HumanMessage
from api.schema import Message, ChatHistory
from uuid import UUID, uuid4


chat = APIRouter()

@chat.get("/")
async def get_chat_list(request : Request):

    # get data from temp db
    db = request.app.state.db
    chathistory = db.get("user_id", {})
    return [
        ChatHistory(thread_id=key, title=chathistory[key]) for key in chathistory
    ]

@chat.get("/{thread_id}")
async def get_chat(thread_id : UUID, request : Request):
    config = {"configurable" : {"thread_id" : thread_id}}
    workflow = request.app.state.workflow
    history = await workflow.aget_state(config)
    if "messages" not in history.values:
        return []
    return [
        Message(id=str(uuid4()), role="human", content=message.content)
        if message.type == "human"
        else Message(id= message.id, role="assistant", content=message.content)
        for message in history.values["messages"]
    ]

@chat.post("/{thread_id}")
async def chat_post(thread_id : UUID, message : Message, request : Request):
    config={"configurable" : {"thread_id" : thread_id}}
    workflow = request.app.state.workflow
    try:
        # save the thread id and title in temp db in app.state.db
        db = request.app.state.db
        if "user_id" not in db:
            db["user_id"] = dict()
        
        if str(thread_id) not in db["user_id"]:
            db["user_id"][str(thread_id)] = message.content


        response = await workflow.ainvoke({"messages": [HumanMessage(content=message.content)]}, config=config)
        return Message(id=response['messages'][-1].id, role="assistant", content=response['messages'][-1].content)
    except Exception as e:
        print(e)
        return Message(role="system", id=str(uuid4()), content="Sorry, there is a problem from our end. :(")
