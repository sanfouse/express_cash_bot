from aiogram.dispatcher.filters.state import StatesGroup, State

class CreditMatching(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    show_result = State()