from aiogram.dispatcher import FSMContext

from data import text
from keyboards.user import default, inline
from loader import bot
from states import distribution
from services.offers_service import get_offers_by_filter

async def question_update_state_data(name, data, state: FSMContext) -> None:
    await state.update_data(
        {
            name: data
        }
    )


async def question1_message_answer(chat_id) -> None:
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
    

async def credit_history_analysis(questions: dict):
    data = {
        'never': -7,
        'often': 3,
        'sometimes': 2,
        'this week': 3,
        'That month': 5,
        'Over a month ago': 1,
        '0': 3,
        '1-5': 3,
        'more than 5': 0,
        'zero percent': 0,
        'default percent': 0
    }

    location = ''
    new_client = True if questions['q1'] == 'never' else False
    zero_percent = True if questions['q4'] == 'zero percent' else False
    bad_credit_history = True if 4 < sum([data[i] for i in questions.values()]) else False

    return await get_offers_by_filter(bad_credit_history, new_client, zero_percent)
    

    

