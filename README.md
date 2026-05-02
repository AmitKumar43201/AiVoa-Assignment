# AI-First CRM — HCP Interaction Logger

An AI-powered Customer Relationship Management (CRM) module for Healthcare Professionals (HCP), built for medical field representatives to log, manage, and query HCP interactions using a conversational chat interface powered by LangGraph and Groq LLMs.

---

## Tech Stack

- **Frontend**: React + Redux Toolkit + React Router + TailwindCSS
- **Backend**: Python + FastAPI
- **AI Agent Framework**: LangGraph
- **LLM**: Groq (`openai/gpt-oss-120b`)
- **Database**: MySQL (via `aiomysql`)
- **Real-time Communication**: WebSocket

---


## Database Schema

```sql
hcp_master       (id, name)
interactions     (id, hcp_id, hcp_name, interaction_type, date, time, sentiment, outcomes)
attendees        (id, interaction_id, name)
topics           (id, interaction_id, topic)
materials        (id, interaction_id, material_name)
samples          (id, interaction_id, sample_name)
followUps        (id, interaction_id, follow_up)
```

All child tables cascade delete on `interaction_id`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send user message to LangGraph agent |
| POST | `/save-data` | Insert or update HCP interaction |
| DELETE | `/delete-data/{hcp_name}` | Delete HCP and all related data |
| WebSocket | `/ws` | Real-time tool event stream |

### Save Data — Upsert Logic
- Check if `hcp_name` exists in `hcp_master` → insert if not
- Check if interaction exists for that HCP → if yes, delete child rows and update; if no, insert
- Re-insert all child rows (attendees, topics, materials, samples, followUps)

---

## LangGraph Agent

### AgentState
```python
class AgentState(BaseModel):
    messages: list = []
    query: str = ''
    intent: Intent = ''
    confidence: int = 0
    response: str = ''
    toolcall: bool = False
    tool_name: str = ''
    tool_param: dict = {}
    tool_message: str = ''
```

### Graph Flow
```
START → intent_node → [Router] → form_node  → tool_node → final_response_node → END
                               → query_node →
                               → END (low confidence)
```

### Intent Classification
| Intent | Routes To |
|--------|-----------|
| `createform` | form_node |
| `editform` | form_node |
| `openform` | form_node |
| `suggestFollowUps` | form_node |
| `querydatabase` | query_node |

---

## Tools

| Tool | Node | Description |
|------|------|-------------|
| `createForm` | form_node | Extracts interaction data from query, emits `createform` event |
| `editForm` | form_node | Extracts partial updates, emits `editform` event |
| `openForm` | form_node | Fetches full form data from DB using HCP name, emits `createform` event |
| `suggestFollowUps` | form_node | Suggests follow-up actions, emits `suggestFollowUps` event |
| `databaseQuery` | query_node | Generates and runs raw SELECT SQL, emits `queryResult` event |

---

## WebSocket Event Flow

```
Frontend → POST /chat → LangGraph runs → tool emits event → WebSocket → Frontend Redux
```

### Events and Redux Handlers

| Event | Redux Action | Effect |
|-------|-------------|--------|
| `createform` | `setForm(data)` | Populates entire form |
| `editform` | `patchForm(data)` | Partially updates form fields |
| `suggestFollowUps` | `patchForm(data)` | Adds/removes follow-ups |
| `queryResult` | `setQueryResults(data)` | Populates table, navigates to `/table` |

---

## Redux — Form Patch Logic

`patchForm` supports structured array operations:

```javascript
// Add/remove items from array fields
dispatch(patchForm({
    attendees: { add: ["Neha"], remove: ["Rohan"] },
    sentiment: "positive"
}))
```

Supports `add`, `remove`, and `replace` operations on all list fields.

---


## Running the Project

### Backend
```bash
cd Backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd Frontend
npm install
npm run dev
```

Make sure MySQL is running and the database is created before starting the backend.
