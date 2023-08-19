from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import ADMIN_IDS


class IsAdmin(BoundFilter):

    key = 'is_admin'

    async def check(self, message: types.Message):
        return str(message.from_user.id) in ADMIN_IDS