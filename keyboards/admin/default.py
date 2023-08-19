from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def add_offer_cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    markup.add(
        KeyboardButton('Отмена')
    )

    return markup


async def menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    markup.add(
        KeyboardButton('Подбор кредита')
    )

    return markup