import uuid

from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from data import text
from filters.is_admin import IsAdmin
from keyboards.admin import default, inline
from loader import bot, dp
from services.offers_service import create_offer
from states import distribution


@dp.message_handler(IsAdmin(), commands='add')
async def admin_add_offer_start(message: types.Message):
    STEP = 1

    await message.answer(text.ADD_OFFER_STEPS[STEP], reply_markup=await default.add_offer_cancel_keyboard())

    await distribution.AddOffer.media_path.set()


@dp.message_handler(IsAdmin(), content_types=['photo'], state=distribution.AddOffer.media_path)
async def admin_add_offer_media_path(message: types.Message, state: FSMContext):
    STEP = 2

    photo_path = f'media/{uuid.uuid4()}.jpg'

    await message.photo[-1].download(photo_path)
    await state.update_data(
            {
                'photo_path': photo_path,
                'photo': message.photo[-1]
            }
        )
    await message.answer(text.ADD_OFFER_STEPS[STEP])

    await distribution.AddOffer.next()


@dp.message_handler(IsAdmin(), state=distribution.AddOffer.description)
async def admin_add_offer_description(message: types.Message, state: FSMContext):
    STEP = 3

    await state.update_data(
            {
                'description': message.text
            }
        )
    await message.answer(
            text.ADD_OFFER_STEPS[STEP],
            reply_markup=await inline.add_offeer_country_list_keyboard()
        )

    await distribution.AddOffer.next()


@dp.callback_query_handler(IsAdmin(), state=distribution.AddOffer.country)
async def admin_add_offer_description(call: types.CallbackQuery, state: FSMContext):
    STEP = 4

    await state.update_data(
            {
                'country': call.data
            }
        )
    await call.message.answer(
            text.ADD_OFFER_STEPS[STEP], 
            reply_markup=await inline.add_offeer_choose_keyboard()
        )

    await distribution.AddOffer.next()


@dp.callback_query_handler(IsAdmin(), state=distribution.AddOffer.new_client)
async def admin_add_offer_new_client(call: types.CallbackQuery, state: FSMContext):
    STEP = 5

    await state.update_data(
            {
                'new_client': bool(int(call.data))
            }
        )
    await call.message.answer(
            text.ADD_OFFER_STEPS[STEP],
            reply_markup=await inline.add_offeer_choose_keyboard()
        )

    await distribution.AddOffer.next()


@dp.callback_query_handler(IsAdmin(), state=distribution.AddOffer.bad_credit_history)
async def admin_add_offer_bad_credit_history(call: types.CallbackQuery, state: FSMContext):
    STEP = 6

    await state.update_data(
            {
                'bad_credit_history': bool(int(call.data))
            }
        )
    await call.message.answer(
            text.ADD_OFFER_STEPS[STEP],
            reply_markup=await inline.add_offeer_choose_keyboard()
        )

    await distribution.AddOffer.next()


@dp.callback_query_handler(IsAdmin(), state=distribution.AddOffer.zero_percent)
async def admin_add_offer_zero_percent(call: types.CallbackQuery, state: FSMContext):
    STEP = 7

    await state.update_data(
            {
                'zero_percent': bool(int(call.data))
            }
        )
    await call.message.answer(text.ADD_OFFER_STEPS[STEP])

    await distribution.AddOffer.next()


@dp.message_handler(IsAdmin(), state=distribution.AddOffer.name)
async def admin_add_offer_message(message: types.Message, state: FSMContext):
    STEP = 8

    await state.update_data(
            {
                'name': message.text
            }
        )
    await message.answer(text.ADD_OFFER_STEPS[STEP])

    await distribution.AddOffer.next()


@dp.message_handler(IsAdmin(), state=distribution.AddOffer.referral_url)
async def admin_add_offer_referral_url(message: types.Message, state: FSMContext):
    await state.update_data(
            {
                'referral_url': message.text
            }
        )
    
    data = await state.get_data()

    await bot.send_photo(
        caption=text.ADD_OFFER_RESULT.format(data['description'], data['referral_url']),
        chat_id=message.from_user.id,
        photo=data['photo'].file_id,
        reply_markup=await default.menu_keyboard()
    )
    await create_offer(
            media_path=data['photo_path'],
            description=data['description'],
            country=data['country'],
            new_client=data['new_client'],
            bad_credit_history=data['bad_credit_history'],
            zero_percent=data['zero_percent'],
            referral_url=data['referral_url'],
            name=data['name']
        )

    await state.finish()


@dp.message_handler(lambda m: m.text == "Отмена", state=distribution.AddOffer)
async def credit_matching_cancel(message: types.Message, state: FSMContext) -> None:
    await message.answer("Отмена", reply_markup=await default.menu_keyboard())

    await state.finish()
