import aiomysql
import globals as g


async def connect_db():
    g.db_pool = await aiomysql.create_pool(
        host="localhost",
        port=3306,
        user="root",
        password="mysql@pass",
        db="assignment",
        autocommit=True
    )
    async with g.db_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1")
            result = await cursor.fetchone()
            if result[0] == 1:
                print("Database connected successfully")
    
async def close_db():
    if g.db_pool:
        g.db_pool.close()
        await g.db_pool.wait_closed()
        g.db_pool = None