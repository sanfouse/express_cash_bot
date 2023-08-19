from aiogram import types
from loader import dp
from filters.is_admin import IsAdmin

@dp.message_handler(IsAdmin(), commands='add')
async def admin_add_offer(message: types.Message):
    await message.answer("You admin!")
