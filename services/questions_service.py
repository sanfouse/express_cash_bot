from aiogram.dispatcher import FSMContext

from data import text
from keyboards.user import default, inline
from loader import bot
from states import distribution
from aiogram import types

async def question_update_state_data(name, data, state: FSMContext):
    await state.update_data(
        {
            name: data
        }
    )


async def question1_message_answer(chat_id):
    await bot.send_message(
            text=text.CREDIT_MATCHING_START_TEXT, 
            reply_markup=await default.credit_mathching_cancel_keyboard(),
            chat_id=chat_id
        )
    await bot.send_message(
            text=text.CREDIT_MATCHING_Q1_TEXT,
            reply_markup=await inline.credit_matching_q1_keyboard(),
            chat_id=chat_id
        )

async def question1_handler(question, chat_id, message_id):
    if question == "never":
        await bot.edit_message_text(
            text=text.CREDIT_MATCHING_Q4_TEXT,
            reply_markup=await inline.credit_matching_q4_keyboard(),
            chat_id=chat_id,
            message_id=message_id
        )
        return distribution.CreditMatching.Q4
    else:
        await bot.edit_message_text(
            text=text.CREDIT_MATCHING_Q2_TEXT,
            reply_markup=await inline.credit_matching_q2_keyboard(),
            chat_id=chat_id,
            message_id=message_id
        )
        return distribution.CreditMatching.Q2
    

    