import asyncio

from data.config import DATABASE_URL
from database.models import db


async def create_db():
    await db.set_bind(DATABASE_URL)
    await db.gino.create_all()

    print("<<< DATABASE CONNECTED")

asyncio.get_event_loop().run_until_complete(create_db())