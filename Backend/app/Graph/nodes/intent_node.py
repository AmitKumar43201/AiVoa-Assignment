from fastapi import  HTTPException
from app.LLM.groq_client import client 
from app.Graph.nodes.schemas import AgentState
import json


from typing import TypedDict
from enum import Enum



class Intent(str, Enum):
    CREATE_FORM = 'createform'
    EDIT_FORM = 'editform'
    OPEN_FORM = 'openform'
    QUERY_DATA = 'querydatabase',
    SUGGEST_FOLLOWUP='suggestFollowUps'
    
class AgentState(TypedDict):
    messages: list = []
    query: str = ''
    intent: Intent = ''
    confidence: int = 0
    response: str = ''
    toolcall: bool = False
    tool_name: str = ''
    tool_param: dict = {} 
    tool_message: str = ''
    tool_id: str = ''


def intent_node(state: AgentState):

    response_format = {
        "type": "json_schema",
        "json_schema": {
        "name": "schema_name",
        "strict": False,
        "schema": {
            "type": 'object',
            "properties": {
                "intent": {"type": "string"},
                "confidence":{"type": "number"}
            }
        }
        }
    }
    messages = [
        {
            "role": "system",
            "content": '''
                You are an intent classifier for an AI form system that logs HCP interactions.

                Classify the user message into one intent:
                - createform: user describes a new interaction to log
                - editform: user wants to modify existing form data
                - openform: user wants to open/view a specific HCP form or they want all the data for one perticular HCP
                - querydatabase: user asks for search/list queries
                - suggestFollowUps: user wants some suggestion about followups

                A plain description of a meeting/call/email means createform.

                Also assign a confidence score from 0 to 5:
                0 = not sure, 5 = very confident

                Return ONLY valid JSON matching the schema.
            '''  
        },
        {
            "role": "user",
            "content": state['query']
        }
    ]
    try:
        res = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            response_format=response_format
        )
        response = json.loads(res.choices[0].message.content)
        
        state['intent'] = response['intent']
        state['confidence']= response["confidence"]
        
        return state
    
    except Exception as e:
        raise HTTPException(e)



if __name__ == "__main__":
   res = intent_node({'query': 'fetch all the data for Dr. Anil Sharma'})
   print(res)