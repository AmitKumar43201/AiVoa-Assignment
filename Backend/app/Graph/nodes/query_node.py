from app.Graph.nodes.schemas import AgentState
from fastapi import HTTPException
from app.Graph.nodes.system_prompts import query_node_system_prompt
from app.LLM.groq_client import client
import json


def query_node(state: AgentState) -> AgentState:
    tool_schema ={
        "type": "function",
        "function": {
            "name": "databaseQuery",
            "description": "Generates and executes a MySQL SELECT query to fetch HCP data from the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {
                        "type": "string",
                        "description": "A valid MySQL SELECT query generated based on user request."
                    }
                },
                "required": ["sql_query"]
            }
        }
    }
    messages = [{'role': "system",'content': query_node_system_prompt}] + state['messages']
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[tool_schema]
        )
        if (response.choices[0].message.tool_calls):
            tool_id = response.choices[0].message.tool_calls[0].id
            tool_name = response.choices[0].message.tool_calls[0].function.name
            tool_argument = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
            state['toolcall'] = True if response.choices[0].message.tool_calls else False
            if  not state['toolcall']:
                return state
            state['tool_id'] = tool_id
            state['tool_name']= tool_name
            state['tool_param'] = tool_argument
            return state
        else:
            return state
    except Exception as e:
       raise HTTPException(e)
        
if __name__ == '__main__':
    query_node(AgentState)