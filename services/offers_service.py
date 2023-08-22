from database.models import Offer
from aiogram import types


async def create_offer(media_path, description, referral_url):
    await Offer.create(
        media_path=media_path,
        description=description,
        referral_url=referral_url
    )


async def get_offers_by_filter(bad_credit_history, new_client, zero_percent):
    offers = await Offer.query.gino.all()
    data = []

    for offer in offers:
        if  offer.bad_credit_history == bad_credit_history if bad_credit_history else True and \
            offer.new_client == new_client and \
            offer.zero_percent == zero_percent:
            data.append(offer)

    return data
            

async def paginate_offers(data, page=1):
    markup = types.InlineKeyboardMarkup()
    pages_count = len(data)

    left  = page-1 if page != 1 else pages_count
    right = page+1 if page != pages_count else 1

    left_button  = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button  = types.InlineKeyboardButton(
            f"{str(page)}/{str(pages_count)}",
            callback_data='_'
        ) 
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    
    markup.add(left_button, page_button, right_button)
    
    return markup

