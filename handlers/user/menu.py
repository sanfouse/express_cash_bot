from aiogram import types
from aiogram.dispatcher import FSMContext

from data import text
from keyboards.user import default, inline
from loader import bot, dp
from services.offers_service import (delete_offer, get_all_offers,
                                     paginate_offers)
from services.questions_service import (credit_history_analysis,
                                        question1_handler,
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
    

@dp.message_handler(lambda m: m.text == 'Список организаций')
async def start(message: types.Message) -> None:
    await message.answer(
            text.CREDIT_LIST_START_MESSAGE, 
            reply_markup=await default.credit_mathching_cancel_keyboard()
        )
    await message.answer(
            text.CREDIT_LIST_MESSAGE, 
            reply_markup=await inline.credit_list_start_keyboard()
        )
    await distribution.CreditMatching.show_result.set()


# ХУКИ ДЛЯ СТАРТА ПОДБОРА КРЕДИТА
@dp.message_handler(lambda m: m.text == 'Подбор кредита')
async def message_credit_matching_state_start(message: types.Message) -> None:
    await message.delete()

    await question1_message_answer(message.from_user.id)
    await distribution.CreditMatching.Q1.set()


@dp.callback_query_handler(lambda c: c.data == "credit_matching_start")
async def callback_credit_matching_state_start(call: types.CallbackQuery) -> None: 
    await call.message.delete()

    await question1_message_answer(call.from_user.id)
    await distribution.CreditMatching.Q1.set()


# State CreditMatching
@dp.callback_query_handler(state=distribution.CreditMatching.Q1)
async def credit_matching_q1(call: types.CallbackQuery, state: FSMContext) -> None:
    data = call.data

    await question_update_state_data('q1', data, state)

    next_question = await question1_handler(data, call.from_user.id, call.message.message_id)
    await next_question.set()


@dp.callback_query_handler(state=distribution.CreditMatching.Q2)
async def credit_matching_q2(call: types.CallbackQuery, state: FSMContext) -> None:
    data = call.data
    
    await question_update_state_data('q2', data, state)
    await call.message.edit_text(
            text.CREDIT_MATCHING_Q3_TEXT,
            reply_markup=await inline.credit_matching_q3_keyboard()
        )
    await distribution.CreditMatching.next()


@dp.callback_query_handler(state=distribution.CreditMatching.Q3)
async def credit_matching_q3(call: types.CallbackQuery, state: FSMContext) -> None:
    data = call.data

    await question_update_state_data('q3', data, state)
    await call.message.edit_text(
            text.CREDIT_MATCHING_Q4_TEXT,
            reply_markup=await inline.credit_matching_q4_keyboard()
        )
    await distribution.CreditMatching.next()


@dp.callback_query_handler(state=distribution.CreditMatching.Q4)
async def credit_matching_q4(call: types.CallbackQuery, state: FSMContext) -> None:
    data = call.data

    await question_update_state_data('q4', data, state)
    await call.message.edit_text(
        text.CREDIT_MATCHING_FINISH_TEXT,
        reply_markup=await inline.credit_matching_show_keyboard()
    )
    await state.update_data(
        {
            'result': await credit_history_analysis(await state.get_data()),
            'chat_id': call.message.chat.id
        }
    )
    await distribution.CreditMatching.next()


@dp.callback_query_handler(
    lambda c: c.data.split(' ')[0].isdigit(), state=distribution.CreditMatching.show_result
)
async def delete_offera_callback(call: types.CallbackQuery, state: FSMContext):
    await delete_offer(int(call.data.split(' ')[0]))
    await state.update_data(
            {
                'result': await get_all_offers()
            }
        )
    await offers_paginate_callback(call, state)


@dp.callback_query_handler(
    lambda c: 'to' in c.data, state=distribution.CreditMatching.show_result
)
async def offers_paginate_callback(call: types.CallbackQuery, state: FSMContext):
    page = int(call.data.split(' ')[1])
    await credit_matching_show_result(
            call.message, page=page, previous_message=call.message, state=state
        )


@dp.callback_query_handler(state=distribution.CreditMatching.show_result)
async def credit_matching_show_result(
        call: types.CallbackQuery, state: FSMContext, page=1, previous_message=None
    ) -> None:
    async def _get_data_result_and_chat_id():
        data = await state.get_data()
        result = data['result']
        chat_id = data['chat_id']
        return result, chat_id    

    try:
        result, chat_id = await _get_data_result_and_chat_id()
    except KeyError:
        await state.update_data(
            {
                'result': await get_all_offers(),
                'chat_id': call.from_user.id
            }
        )
    finally:
        result, chat_id = await _get_data_result_and_chat_id()
    try:
        offer = result[page - 1]
        markup = await paginate_offers(chat_id in [895872844], result, offer, page)

        try: 
            try: photo = open(offer.media_path, 'rb')
            except: photo = offer.media_path
            await bot.send_photo(
                    chat_id,
                    photo=photo,
                    caption=offer,
                    reply_markup=markup
                )
        except: 
            await bot.send_message(
                    chat_id,
                    offer,
                    reply_markup=markup
                )
        try: await bot.delete_message(chat_id, previous_message.message_id)
        except AttributeError: pass
    except IndexError:
        await bot.send_message(
            chat_id,
            text.CREDIT_MATCHING_SHOW_TEXT,
            reply_markup=await default.menu_keyboard()
        )
        await state.finish()


# Cancel CreditMatching
@dp.message_handler(lambda m: m.text == "Отмена", state=distribution.CreditMatching)
async def credit_matching_cancel(message: types.Message, state: FSMContext) -> None:
    await message.answer("Отмена", reply_markup=await default.menu_keyboard())

    await state.finish()