from database.models import Offer
from aiogram import types


async def create_offer(
            media_path,
            description, 
            country, 
            new_client, 
            bad_credit_history, 
            zero_percent, 
            referral_url,
            name
        ) -> None:
    
    await Offer.create(
        media_path=media_path,
        description=description,
        country=int(country),
        new_client=new_client,
        bad_credit_history=bad_credit_history,
        zero_percent=zero_percent,
        referral_url=referral_url,
        name=name
    )


async def delete_offer(idx):
    await Offer.delete.where(Offer.idx == idx).gino.status()


async def get_all_offers():
    return await Offer.query.gino.all()


async def get_offers_by_filter(bad_credit_history, new_client, zero_percent):
    offers = await Offer.query.gino.all()
    data = set()

    for offer in offers:
        if  (offer.bad_credit_history == bad_credit_history if bad_credit_history else True) and \
            (offer.new_client == new_client) and \
            (offer.zero_percent == zero_percent):
            data.add(offer)
        if new_client and (offer.new_client == new_client):
            data.add(offer)

    return list(data)
            

async def paginate_offers(admin, data, offer, page=1) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    pages_count = len(data)

    left  = page-1 if page != 1 else pages_count
    right = page+1 if page != pages_count else 1

    if admin:
        markup.add(
            types.InlineKeyboardButton(
                'Удалить [ADMIN ONLY]', callback_data=f"{offer.idx} {page}"
            )
        )

    markup.add(
        types.InlineKeyboardButton(
            'Получить займ!', url=offer.referral_url
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "←", callback_data=f'to {left}'
        ),
        types.InlineKeyboardButton(
            f"{str(page)}/{str(pages_count)}",
            callback_data=''
        ), 
        types.InlineKeyboardButton(
            "→", callback_data=f'to {right}'
        )
    )
    
    return markup

