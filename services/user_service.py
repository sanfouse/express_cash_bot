from database.models import User
from aiogram import types

async def check_user_exist(message: types.Message):
    if not await User.query.where(User.idx == message.from_user.id).gino.first():
        await User.create(
            idx=message.from_user.id,
            username=message.from_user.username
        )