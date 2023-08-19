import uuid

from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from data import text
from filters.is_admin import IsAdmin
from loader import dp, bot
from states import distribution
from keyboards.admin import default
from services.offers_service import create_offer


@dp.message_handler(IsAdmin(), commands='add')
async def admin_add_offer_start(message: types.Message):
    await message.answer(text.ADD_OFFER_PHOTO_TEXT, reply_markup=await default.add_offer_cancel_keyboard())

    await distribution.AddOffer.photo.set()


@dp.message_handler(IsAdmin(), content_types=['photo'], state=distribution.AddOffer.photo)
async def admin_add_offer_photo(message: types.Message, state: FSMContext):
    photo_path = f'media/{uuid.uuid4()}.jpg'

    await message.photo[-1].download(photo_path)
    await state.update_data(
            {
                'photo_path': photo_path,
                'photo': message.photo[-1]
            }
        )
    await message.answer(text.ADD_OFFER_DESCRIPTION_TEXT)

    await distribution.AddOffer.next()


@dp.message_handler(IsAdmin(), state=distribution.AddOffer.description)
async def admin_add_offer_description(message: types.Message, state: FSMContext):
    await state.update_data(
            {
                'description': message.text
            }
        )
    await message.answer(text.ADD_OFFER_URL_TEXT)

    await distribution.AddOffer.next()


@dp.message_handler(IsAdmin(), state=distribution.AddOffer.url)
async def admin_add_offer_url(message: types.Message, state: FSMContext):
    await state.update_data(
            {
                'url': message.text
            }
        )
    
    data = await state.get_data()

    await bot.send_photo(
        caption=text.ADD_OFFER_RESULT.format(data['description'], data['url']),
        chat_id=message.from_user.id,
        photo=data['photo'].file_id,
        reply_markup=await default.menu_keyboard()
    )

    await create_offer(data['photo_path'], data['description'], data['url'])

    await state.finish()


@dp.message_handler(lambda m: m.text == "Отмена", state=distribution.AddOffer)
async def credit_matching_cancel(message: types.Message, state: FSMContext) -> None:
    await message.answer("Отмена", reply_markup=await default.menu_keyboard())

    await state.finish()
