import os
from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from workflow import workflow
from .chat import chat


DB_URI = os.getenv("CHECKPOINTER_DB_URI", "")

@asynccontextmanager
async def lifespan(api : FastAPI):
    async with AsyncMongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        api.state.workflow = workflow.compile(checkpointer=checkpointer)
        yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(chat, prefix="/chat")

if __name__ == "__main__":
    pass
