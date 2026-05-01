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