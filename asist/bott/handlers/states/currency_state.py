from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import hbold

from asist.bott.include import F, FSMContext, Message
from asist.bott.core import router, bot_
from asist.bott.keyboards import constructor_kb

from asist.bott.texts import currency_dict
from .clock_state import ClockState


class CountMoneyState(StatesGroup):
    wait_number = State()

@router.message(CountMoneyState.wait_number, F.text)
async def catch_time(message: Message, state: FSMContext):
    msg_txt = message.text
    await bot_.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    try:
        number = float(msg_txt.replace('-', ''))
    except ValueError:
        await bot_.edit_message_text(
            chat_id=message.chat.id,
            message_id=(await state.get_data())['id'],
            text="Неверный формат❗️",
            reply_markup=constructor_kb(
                cancel=True,
                prefix_cancel=(await state.get_data())['kb_text']
            )
        )
        await state.set_state(ClockState.alarm_clock_time)
        return

    curr = (await state.get_data())['currency']
    exchange_rate: float = (await state.get_data())['rate']
    action: str = (await state.get_data())['action']
    currency_in: str = currency_dict[curr]
    currency_out: str = currency_dict[
        (await state.get_data())['currency'].replace(
            f'{"in" if "in" in curr else "out"}',
            f'{"out" if "in" in curr else "in"}'
        )
    ]

    if action.replace('_in', '').replace('_out', '') in ['USD_RUB', 'RUB_EUR', 'RUB_EUR', 'USD_RUB']:
        result = exchange_rate * number
    elif action.replace('_in', '').replace('_out', '') in ['USD', 'EUR']:
        if 'in' in action:
            result = exchange_rate * number
        else:
            result = number / exchange_rate
    else:
        if 'in' in action:
            result = exchange_rate/100 * number
        else:
            result = number / exchange_rate*100

    await bot_.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data())['id'],
        text=hbold(f'{number}{currency_in} = {round(result, 2)}{currency_out}'),
        reply_markup=constructor_kb(
            data={
                'Назад': 'calculate',
                'Главное меню': 'main_menu'
            },
            join=False
        )
    )

    await state.clear()