[Graph code]
class Intent(str, Enum):
    CREATE_FORM = 'createform'
    EDIT_FORM = 'editform'
    OPEN_FORM = 'openform'
    QUERY_DATA = 'querydatabase'

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
    
from fastapi import  HTTPException
from app.LLM.groq_client import client
from pydantic import BaseModel  
import json
from app.Graph.nodes.schemas import AgentState


def intent_node(state: AgentState):

    messages = [
        {
            "role": "user",
            "content": state['query']
        }
    ]
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            response_format=response_format
        )
        response = json.loads(res.choices[0].message.content)
        
        state['intent'] = response['intent']
        state['confidence ']= response["confidence"]
        
        return state
    
    except Exception as e:
        raise HTTPException(e)
    

def form_node(state: AgentState) -> AgentState:

    messages = [{"role": "system","content": form_node_system_prompt}] + state['messages']
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[create_form,edit_form,suggest_folloups,open_form_schema]
        )
        tool_name = response.choices[0].message.tool_calls[0].function.name
        tool_argument = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        state['toolcall'] = True if response.choices[0].message.tool_calls else False
        if not state['toolcall']:
            return state
        else:
            state['tool_name ']= tool_name
            state['tool_argument']= tool_argument
            return state
    except Exception as e:
        raise HTTPException(e)
    
def query_node(state: AgentState) -> AgentState:

    messages = [{'role': "system",'content': query_node_system_prompt}] + state['messages']
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[tool_schema]
        )
        tool_name = response.choices[0].message.tool_calls[0].function.name
        tool_argument = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        state['toolcall'] = True if response.choices[0].message.tool_calls else False
        if  not state['toolcall']:
            return state
        state['tool_name']= tool_name
        state[tool_argument] = tool_argument
        return state
    except Exception as e:
        HTTPException(e)
        
async def tools_node(state: AgentState) -> AgentState:
    TOOL_MAP = {
    "createForm": createForm,
    "editForm": editForm,
    "openForm": openForm,
    "suggestFollowUps": suggestFollowUps,
    "databaseQuery": databaseQuery,
    }
    
    async def tool_orchestrator():
        tool_name = state['tool_name']
        params = state['tool_param']

        print(f"Calling tool: {tool_name} with params: {params}")

        tool_fn = TOOL_MAP.get(tool_name)
        if tool_fn:
            tool_message = await tool_fn(params)
            return tool_message
        else:
            print(f"Unknown tool: {tool_name}")
    if state['tool_name'] and state['tool_param']:          
        tool_message =  await tool_orchestrator()
        state['tool_message']= tool_message
        return state
    else: 
        return state
    
def final_response_node(state: AgentState):
    messages = state['messages']
    sys = [{"role": "system", "content": final_res_node}]
    if state['tool_message']:
        tool_message=[{"role":'toolcall', "content": state['tool_message']}]
    messages = sys + messages + tool_message
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
        )
        content = response.choices[0].message.content
        if content:
            state['messages'].append({"role": "assistant", "content": content} )
    except Exception as e:
        raise HTTPException(e)
    
    def Router(state: AgentState):
    if state['intent'] == Intent.CREATE_FORM or state['intent'] == Intent.EDIT_FORM and state['confidence'] >= 4:
        return "form"
    elif state['intent'] == Intent.QUERY_DATA and state['confidence'] >= 4:
        return "query"
    else:
        state['response'] = "Please provide more information"
        return "end"


def get_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("intent_node", intent_node)
    graph.add_node("form_node", form_node)
    graph.add_node("query_node", query_node)
    graph.add_node("tools_node", tools_node)
    graph.add_node("final_response_node", final_response_node)

    graph.add_edge(START, "intent_node")
    graph.add_conditional_edges(
        "intent_node",
        Router,
        {
            "end": END,
            "form": "form_node",
            "query": "query_node"
        }
    )
    graph.add_edge("query_node", "tools_node")
    graph.add_edge("form_node", "tools_node")
    graph.add_edge("tools_node", "final_response_node")
    graph.add_edge("final_response_node", END)
    
    app = graph.compile()
    
    return app


