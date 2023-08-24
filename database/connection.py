import asyncio

from data.config import DATABASE_URL
from database.models import db

from database.models import Country


async def create_countries():
    try:
        await Country.create(
                idx=1, name = 'Россия'
            )
        await Country.create(
            idx=2, name = 'Украина'
        )
        await Country.create(
            idx=3, name = 'Казахстан'
        )
    except: pass


async def create_db():
    await db.set_bind(DATABASE_URL)
    await db.gino.create_all()
    await create_countries()
    print("<<< DATABASE CONNECTED")

asyncio.get_event_loop().run_until_complete(create_db())