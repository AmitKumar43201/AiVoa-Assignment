from app.Graph.nodes.schemas import AgentState
from app.LLM.groq_client import client
from fastapi import HTTPException
from app.Graph.nodes.system_prompts import final_res_node


def final_response_node(state: AgentState):
    messages = state['messages']
    sys = [{"role": "system", "content": final_res_node}]
    tool_message=[{"role":'tool',"tool_call_id":state['tool_id'],"name":state['tool_name'], "content": state['tool_message']}]  if state['tool_message'] else []
    messages = sys + messages + tool_message
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
        )
        content = response.choices[0].message.content
        if content:
            state['messages'].append({"role": "assistant", "content": content} )
        return state
    except Exception as e:
        raise HTTPException(e)