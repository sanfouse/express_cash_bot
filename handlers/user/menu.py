from aiogram import types
from aiogram.dispatcher import FSMContext

from data import text
from keyboards.user import default, inline
from loader import dp
from services.questions_service import (question1_handler,
                                        question1_message_answer,
                                        question_update_state_data)
from services.user_service import check_user_exist
from states import distribution


@dp.message_handler(commands='start')
async def start(message: types.Message) -> None:
    await check_user_exist(message)
    await message.answer(text.START_MESSAGE, reply_markup=await default.menu_keyboard())
    await message.answer(
            text.CREDIT_MATCHING_DESCRIPTION,
            reply_markup=await inline.credit_matching_start_keyboard()
        )


# ХУКИ ДЛЯ СТАРТА ПОДБОРА КРЕДИТА
@dp.message_handler(lambda m: m.text == 'Подбор кредита')
async def message_credit_matching_state_start(message: types.Message) -> None:
    await message.answer(text.CREDIT_MATCHING_TEXT)
    await question1_message_answer(message.from_user.id)
    await distribution.CreditMatching.Q1.set()


@dp.callback_query_handler(lambda c: c.data == "credit_matching_start")
async def callback_credit_matching_state_start(call: types.CallbackQuery) -> None:
    await question1_message_answer(call.from_user.id)
    await distribution.CreditMatching.Q1.set()


# State CreditMatching
@dp.callback_query_handler(state=distribution.CreditMatching.Q1)
async def credit_matching_q1(call: types.CallbackQuery, state: FSMContext):
    data = call.data

    await question_update_state_data('q1', data, state)

    next_question = await question1_handler(data, call.from_user.id, call.message.message_id)
    await next_question.set()


@dp.callback_query_handler(state=distribution.CreditMatching.Q2)
async def credit_matching_q2(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    
    await question_update_state_data('q2', data, state)
    await call.message.edit_text(
            text.CREDIT_MATCHING_Q3_TEXT,
            reply_markup=await inline.credit_matching_q3_keyboard()
        )
    await distribution.CreditMatching.next()


@dp.callback_query_handler(state=distribution.CreditMatching.Q3)
async def credit_matching_q3(call: types.CallbackQuery, state: FSMContext):
    data = call.data

    await question_update_state_data('q3', data, state)
    await call.message.edit_text(
            text.CREDIT_MATCHING_Q4_TEXT,
            reply_markup=await inline.credit_matching_q4_keyboard()
        )
    await distribution.CreditMatching.next()

@dp.callback_query_handler(state=distribution.CreditMatching.Q4)
async def credit_matching_q4(call: types.CallbackQuery, state: FSMContext):
    data = call.data

    await question_update_state_data('q4', data, state)
    await call.message.edit_text(
        text.CREDIT_MATCHING_FINISH_TEXT,
        reply_markup=await inline.credit_matching_show_keyboard()
    )
    await distribution.CreditMatching.next()


@dp.callback_query_handler(state=distribution.CreditMatching.show_result)
async def credit_matching_show_result(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    await call.message.answer(
            text.CREDIT_MATCHING_SHOW_TEXT, reply_markup=await default.menu_keyboard()
        )
    await state.finish()


# Cancel CreditMatching
@dp.message_handler(lambda m: m.text == "Отмена", state=distribution.CreditMatching)
async def credit_matching_cancel(message: types.Message, state: FSMContext):
    await message.answer("Отмена", reply_markup=await default.menu_keyboard())

    await state.finish()