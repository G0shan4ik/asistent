from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Финансы💸")],
            [KeyboardButton(text="Мои планы🌵")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True
        )