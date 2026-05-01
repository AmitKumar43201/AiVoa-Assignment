from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date, time
import globals as g

db_roots = APIRouter()

class InteractionForm(BaseModel):
    hcp_name: str
    interaction_type: str
    date: date
    time: str
    attendees: List[str]
    topics: List[str]
    materials: List[str]
    samples: List[str]
    sentiment: str
    outcomes: str
    followUps: List[str]
    
@db_roots.post("/save-data")
async def save_data(form: InteractionForm):
    async with g.db_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # 1. Get or create HCP
            await cursor.execute("SELECT id FROM hcp_master WHERE name = %s", (form.hcp_name,))
            hcp = await cursor.fetchone()
            if not hcp:
                await cursor.execute("INSERT INTO hcp_master (name) VALUES (%s)", (form.hcp_name,))
                hcp_id = cursor.lastrowid
            else:
                hcp_id = hcp[0]

            # 2. Check if interaction exists
            await cursor.execute("SELECT id FROM interactions WHERE hcp_id = %s", (hcp_id,))
            interaction = await cursor.fetchone()

            if interaction:
                interaction_id = interaction[0]
                # Update main interaction
                await cursor.execute("""
                    UPDATE interactions 
                    SET interaction_type=%s, date=%s, time=%s, sentiment=%s, outcomes=%s
                    WHERE id=%s
                """, (form.interaction_type, form.date, form.time, form.sentiment, form.outcomes, interaction_id))
                # Delete child rows
                for table in ["attendees", "topics", "materials", "samples", "followUps"]:
                    await cursor.execute(f"DELETE FROM {table} WHERE interaction_id = %s", (interaction_id,))
            else:
                # Insert new interaction
                await cursor.execute("""
                    INSERT INTO interactions (hcp_id, hcp_name, interaction_type, date, time, sentiment, outcomes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (hcp_id, form.hcp_name, form.interaction_type, form.date, form.time, form.sentiment, form.outcomes))
                interaction_id = cursor.lastrowid

            # 3. Insert child rows
            for attendee in form.attendees:
                await cursor.execute("INSERT INTO attendees (interaction_id, name) VALUES (%s, %s)", (interaction_id, attendee))
            for topic in form.topics:
                await cursor.execute("INSERT INTO topics (interaction_id, topic) VALUES (%s, %s)", (interaction_id, topic))
            for material in form.materials:
                await cursor.execute("INSERT INTO materials (interaction_id, material_name) VALUES (%s, %s)", (interaction_id, material))
            for sample in form.samples:
                await cursor.execute("INSERT INTO samples (interaction_id, sample_name) VALUES (%s, %s)", (interaction_id, sample))
            for follow_up in form.followUps:
                await cursor.execute("INSERT INTO followUps (interaction_id, follow_up) VALUES (%s, %s)", (interaction_id, follow_up))

    return {"message": "Interaction saved successfully", "interaction_id": interaction_id}

@db_roots.delete("/delete-data/{hcp_name}")
async def delete_data(hcp_name: str):
    async with g.db_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT id FROM hcp_master WHERE name = %s", (hcp_name,))
            hcp = await cursor.fetchone()
            if not hcp:
                raise HTTPException(status_code=404, detail="HCP not found")
            
            hcp_id = hcp[0]
            await cursor.execute("SELECT id FROM interactions WHERE hcp_id = %s", (hcp_id,))
            interaction = await cursor.fetchone()
            if interaction:
                await cursor.execute("DELETE FROM interactions WHERE hcp_id = %s", (hcp_id,))

            await cursor.execute("DELETE FROM hcp_master WHERE id = %s", (hcp_id,))

    return {"message": f"HCP '{hcp_name}' and all interactions deleted successfully"}


