from database.models import Offer


async def create_offer(media_path, description, referral_url):

    await Offer.create(
        media_path=media_path,
        description=description,
        referral_url=referral_url
    )