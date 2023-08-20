from database.models import Offer


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
            

