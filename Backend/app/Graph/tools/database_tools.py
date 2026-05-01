import aiomysql
from globals import emit
import globals as g
import asyncio

async def create_table_data(params: dict):
    hcp_name = params["name"] if params["name"] else params["hcp_name"]
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

            # Attendeesb 
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

    return form_data



async def databaseQuery(params: dict):
    sql_query = params["sql_query"]

    async with g.db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(sql_query)
            results = await cursor.fetchall()

    serialized = []
    for row in results:
        serialized.append({k: str(v) if v is not None else None for k, v in row.items()})
    print(serialized)
    data_list = await asyncio.gather(*[create_table_data(row) for row in serialized])
    data_list = [d for d in data_list if d is not None]

    await emit("queryResult", data_list)
    
    return "Queryied the database and sent the result"