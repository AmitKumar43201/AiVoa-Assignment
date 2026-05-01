from langgraph.graph import StateGraph, START, END
from app.Graph.nodes.schemas import AgentState, Intent
from app.Graph.nodes import intent_node, form_node, query_node, final_response_node, tools_node
    
def Router(state: AgentState):
    if state['intent'] == Intent.CREATE_FORM or state['intent'] == Intent.EDIT_FORM or state["intent"] == Intent.OPEN_FORM or state["intent"] == Intent.SUGGEST_FOLLOWUP and state['confidence'] >= 4:
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

