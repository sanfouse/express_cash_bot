from aiogram.dispatcher.filters.state import StatesGroup, State
from typing import List


class CreditMatching(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    show_result = State()


class AddOffer(StatesGroup):
    media_path = State()

    description = State()    
    country = State()

    new_client = State()
    bad_credit_history = State()
    zero_percent = State()

    name = State()
    referral_url = State()
