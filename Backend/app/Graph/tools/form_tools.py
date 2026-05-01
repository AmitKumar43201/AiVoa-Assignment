import aiomysql
from globals import emit
import globals as g

async def createform(params: dict):
    await emit("createform", params)
    return "Created the form"

async def editform(params: dict):
    await emit("editform", params)
    return 'Updated the form'

async def suggestFollowUps(params: dict):
    await emit("suggestFollowUps", params)
    return "Sent the followups suggestions"

async def openForm(params: dict):
    hcp_name = params["hcp_name"]
    search = f"%{hcp_name.lower()}%"
    
    async with g.db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            # Main interaction
            await cursor.execute("""
                SELECT i.* FROM interactions i
                JOIN hcp_master h ON i.hcp_id = h.id
                WHERE LOWER(h.name) LIKE %s
            """, (search,))
            interaction = await cursor.fetchone()

            if not interaction:
                await emit("error", {"message": f"No form found for {hcp_name}"})
                return

            interaction_id = interaction["id"]

            # Attendees
            await cursor.execute("SELECT name FROM attendees WHERE interaction_id = %s", (interaction_id,))
            attendees = [row["name"] for row in await cursor.fetchall()]

            # Topics
            await cursor.execute("SELECT topic FROM topics WHERE interaction_id = %s", (interaction_id,))
            topics = [row["topic"] for row in await cursor.fetchall()]

            # Materials
            await cursor.execute("SELECT material_name FROM materials WHERE interaction_id = %s", (interaction_id,))
            materials = [row["material_name"] for row in await cursor.fetchall()]

            # Samples
            await cursor.execute("SELECT sample_name FROM samples WHERE interaction_id = %s", (interaction_id,))
            samples = [row["sample_name"] for row in await cursor.fetchall()]

            # Follow-ups
            await cursor.execute("SELECT follow_up FROM followUps WHERE interaction_id = %s", (interaction_id,))
            followUps = [row["follow_up"] for row in await cursor.fetchall()]

    form_data = {
        "hcp_name": interaction["hcp_name"],
        "interaction_type": interaction["interaction_type"],
        "date": str(interaction["date"]),
        "time": str(interaction["time"]),
        "attendees": attendees,
        "topics": topics,
        "materials": materials,
        "samples": samples,
        "sentiment": interaction["sentiment"],
        "outcomes": interaction["outcomes"],
        "followUps": followUps
    }

    await emit("createform", form_data)
    return "Opened the form successfuly"


