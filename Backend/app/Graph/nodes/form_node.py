from fastapi import HTTPException
from app.Graph.nodes.schemas import AgentState
from app.Graph.nodes.system_prompts import form_node_system_prompt
from app.LLM.groq_client import client
import json

def form_node(state: AgentState) -> AgentState:
    create_form = {
        "type": "function",
        "function": {
            "name": "createform",
            "description": "Creates a form entry for an HCP (Healthcare Professional) interaction. Extract all available details from the user's query to populate the fields.",
            "parameters": {
            "type": "object",
            "properties": {
                "hcp_name": {
                "type": "string",
                "description": "The name or identifier of the Healthcare Professional (HCP) involved in the interaction."
                },
                "interaction_type": {
                "type": "string",
                "enum": ["Meeting", "Call", "Email", "Conference", "Virtual"],
                "description": "The type of interaction with the HCP."
                },
                "attendees": {
                "type": "array",
                "items": { "type": "string" },
                "description": "List of people who attended or were part of the interaction."
                },
                "topics": {
                "type": "array",
                "items": { "type": "string" },
                "description": "List of topics discussed during the interaction."
                },
                "materials": {
                "type": "array",
                "items": { "type": "string" },
                "description": "List of materials shared or used during the interaction."
                },
                "samples": {
                "type": "array",
                "items": { "type": "string" },
                "description": "List of product samples provided during the interaction."
                },
                "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negetive"],
                "description": "The overall sentiment or tone of the interaction."
                },
                "outcomes": {
                "type": "string",
                "description": "Summary of the outcomes or results from the interaction."
                },
                "followUps": {
                "type": "array",
                "items": { "type": "string" },
                "description": "Any follow-up actions or next steps agreed upon after the interaction."
                }
            },
            "required": ["hcp_name"]
            }
        }
        }
    
    edit_form = {
        "type": "function",
        "function": {
            "name": "editform",
            "description": "Edits an existing HCP interaction form. Only include fields that the user wants to change. For interactionType and sentiment, provide the new value directly. For outcomes and followUp, provide the new text value directly. For attendees, topics, materials, and samples, specify items to add and/or remove using nested add/remove arrays.",
            "parameters": {
            "type": "object",
            "properties": {
                "interaction_type": {
                "type": "string",
                "enum": ["Meeting", "Call", "Email", "Conference", "Virtual"],
                "description": "New interaction type to replace the current one."
                },
                "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative"],
                "description": "New sentiment to replace the current one."
                },
                "outcomes": {
                "type": "string",
                "description": "New value to replace the current outcomes text."
                },
                "follwUps": {
                "type": "object",
                "description": "Add or remove followups. Include only the keys needed.",
                "properties": {
                    "add": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of followups to add."
                    },
                    "remove": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of followups to remove."
                    }
                },
                "additionalProperties": False
                },
                "attendees": {
                "type": "object",
                "description": "Add or remove attendees. Include only the keys needed.",
                "properties": {
                    "add": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of attendees to add."
                    },
                    "remove": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of attendees to remove."
                    }
                },
                "additionalProperties": False
                },
                "topics": {
                "type": "object",
                "description": "Add or remove topics. Include only the keys needed.",
                "properties": {
                    "add": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of topics to add."
                    },
                    "remove": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of topics to remove."
                    }
                },
                "additionalProperties": False
                },
                "materials": {
                "type": "object",
                "description": "Add or remove materials. Include only the keys needed.",
                "properties": {
                    "add": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of materials to add."
                    },
                    "remove": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of materials to remove."
                    }
                },
                "additionalProperties": False
                },
                "samples": {
                "type": "object",
                "description": "Add or remove samples. Include only the keys needed.",
                "properties": {
                    "add": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of samples to add."
                    },
                    "remove": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "List of samples to remove."
                    }
                },
                "additionalProperties": False
                }
            },
            "additionalProperties": False
            }
        }
        }
    
    suggest_followups = {
        "type": "function",
        "function": {
            "name": "suggestFollowUps",
            "description": "Suggests, adds, or removes follow-up actions based on the HCP interaction context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "followUps": {
                        "type": "object",
                        "description": "Add or remove followups. Include only the keys needed.",
                        "properties": {
                            "add": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of followups to add."
                            },
                            "remove": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of followups to remove."
                            }
                        },
                        "additionalProperties": False
                    }
                },
                "required": ["followUps"]
            }
        }
    }
    open_form_schema = {
    "type": "function",
    "function": {
        "name": "openForm",
        "description": "Fetches complete form data for a specific HCP by running predefined queries across all tables.",
        "parameters": {
            "type": "object",
            "properties": {
                "hcp_name": {
                    "type": "string",
                    "description": "The name of the HCP whose form needs to be opened."
                }
            },
            "required": ["hcp_name"]
        }
    }
}
    messages = [{"role": "system","content": form_node_system_prompt}] + state['messages']
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[create_form,edit_form,suggest_followups,open_form_schema]
        )
        tool_id = response.choices[0].message.tool_calls[0].id
        tool_name = response.choices[0].message.tool_calls[0].function.name
        tool_argument = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        state['toolcall'] = True if response.choices[0].message.tool_calls else False
        if not state['toolcall']:
            return state
        else:
            state['tool_name']= tool_name
            state['tool_param']= tool_argument
            state['tool_id'] = tool_id
            return state
    except Exception as e:
        raise HTTPException(e)
    
if __name__ == '__main__':
    form_node(AgentState) 