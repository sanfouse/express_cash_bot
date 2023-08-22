from database import models
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def add_offeer_country_list_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Россия',
            callback_data='1'
        ),
        InlineKeyboardButton(
            text='Казахстан',
            callback_data='2'
        ),
        InlineKeyboardButton(
            text='Украина',
            callback_data='3'
        )
    )

    return markup


async def add_offeer_choose_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Да',
            callback_data='1'
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data='0'
        )
    )

    return markup