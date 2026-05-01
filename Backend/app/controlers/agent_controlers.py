from fastapi import APIRouter
from pydantic import BaseModel
from app.Graph.graph import get_agent_graph

agent_routes = APIRouter()

class RequestType(BaseModel):
    messages: list
@agent_routes.post('/message')
async def agent(request: RequestType):
    messages = request.messages
    initial_state = {
        "messages": messages,
        "query": messages[-1]['content'],
        "intent": '',
        "confidence": 0,
        "response": '',
        "toolcall": False,
        "tool_name": '',
        "tool_param": {},
        "tool_message": '',
        "tool_id": ''
    }
    
    agent = get_agent_graph()
    response = await agent.ainvoke(initial_state)  # use ainvoke for async
    
    return {
        "data": response['messages'][-1]
    }
