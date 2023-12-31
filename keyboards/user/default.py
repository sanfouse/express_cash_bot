from database import models
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


async def menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    
    markup.add(
        KeyboardButton('Подбор кредита'),
        KeyboardButton('Список организаций')
    )

    return markup

async def credit_mathching_cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    markup.add(
        KeyboardButton('Отмена')
    )

    return markup