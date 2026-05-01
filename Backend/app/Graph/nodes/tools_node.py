from app.Graph.nodes.schemas import AgentState
import globals as g
from app.Graph.tools.database_tools import databaseQuery
from app.Graph.tools.form_tools import createform, editform, suggestFollowUps, openForm

async def tools_node(state: AgentState) -> AgentState:
    TOOL_MAP = {
    "createform": createform,
    "editform": editform,
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