from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .helpers import chunks


def start_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Финансы🤑',
                                     callback_data=f'finances'),
                InlineKeyboardButton(text='Check in☑️',
                                     callback_data=f'check_in')
            ],
            [InlineKeyboardButton(text='Курсы валют📉', callback_data=f'currency')],
            [InlineKeyboardButton(text='Будильник⏰', callback_data=f'clock')]
        ]
    )

def constructor_kb(
        data: Optional[dict] = None,
        join: bool = True,
        num: int = 1,
        cancel: bool = False,
        name_cancel: str = 'Назад',
        prefix_cancel: str = 'main_menu'
):
    inline_keyboard = []
    if cancel and not data:
        inline_keyboard = [
            [InlineKeyboardButton(text=name_cancel, callback_data=prefix_cancel)]
        ]
    elif data:
        if join:
            inline_keyboard = [
                [InlineKeyboardButton(
                    text=btn, callback_data=call_data) for btn, call_data in data.items()]
            ]
        else:
            buttons = [InlineKeyboardButton(
                text=btn, callback_data=call_data) for btn, call_data in
                data.items()]

            inline_keyboard = [btn for btn in chunks(lst=buttons, n=num)]
        if cancel:
            inline_keyboard.append([InlineKeyboardButton(text=name_cancel, callback_data=prefix_cancel)])

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )


def get_kb_with_scroll(mass: list[list], idx: int):
    btn_left, btn_right = '«', '»'

    if not mass:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='main_menu')]
            ]
        )

    buttons = [
        InlineKeyboardButton(
            text=data[0], callback_data=f"_note${data[-1]}")
            for data in mass[idx]
            for _ in range(1)
    ]
    inline_keyboard = [btn for btn in chunks(lst=buttons, n=2)]

    if len(mass) == 1:
        inline_keyboard.append(
            [InlineKeyboardButton(text='Назад', callback_data='main_menu')]
        )
        return InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )
    elif idx == 0 and len(mass) > 1:
        inline_keyboard.append(
            [InlineKeyboardButton(text=btn_right, callback_data=f'note${idx+1}')]
        )
    elif idx == len(mass) - 1:
        inline_keyboard.append(
            [InlineKeyboardButton(text=btn_left, callback_data=f'note${idx-1}')]
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=btn_left, callback_data=f'note${idx - 1}'),
                InlineKeyboardButton(text=btn_right, callback_data=f'note${idx+1}')
            ]
        )

    inline_keyboard.append(
        [InlineKeyboardButton(text='Назад', callback_data='main_menu')]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
