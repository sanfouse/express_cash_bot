from database import models
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

async def credit_matching_start_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Подбор кредита',
            callback_data='credit_matching_start'
        )
    )

    return markup


async def credit_matching_q1_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Никогда не брал займ',
            callback_data='never'
        ),
        InlineKeyboardButton(
            text='Регулярно брал',
            callback_data='often'
        ),
        InlineKeyboardButton(
            text='Редко',
            callback_data='sometimes'
        )
    )

    return markup


async def credit_matching_q2_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='На этой неделе',
            callback_data='this week'
        ),
        InlineKeyboardButton(
            text='В том месяце',
            callback_data='That month'
        ),
        InlineKeyboardButton(
            text='Больше месяца назад',
            callback_data='Over a month ago'
        )
    )

    return markup

async def credit_matching_q3_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='0',
            callback_data='0'
        ),
        InlineKeyboardButton(
            text='1-5',
            callback_data='1-5'
        ),
        InlineKeyboardButton(
            text='более 5',
            callback_data='more than 5'
        )
    )

    return markup

async def credit_matching_q4_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Займы под 0%',
            callback_data='zero percent'
        ),
        InlineKeyboardButton(
            text='Обычный процент',
            callback_data='default percent'
        )
    )

    return markup


async def credit_matching_show_keyboard():

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='Показать',
            callback_data='show'
        )
    )

    return markup
