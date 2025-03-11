from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import hbold
from watchfiles import awatch

from asist.bott.include import F, FSMContext, Message, START_CHECK_IN_TEXT
from asist.bott.mixins.check_in_mixin import CheckInMixin
from asist.bott.core import router, bot_
from asist.bott.keyboards import constructor_kb
from asist.bott.helpers import TimeManager

from asist.bott.texts import currency_dict


# <--- Clock State --->
class ClockState(StatesGroup):
    alarm_clock_time = State()

@router.message(ClockState.alarm_clock_time, F.text)
async def catch_time(message: Message, state: FSMContext):
    await bot_.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    _hours, _minutes = message.text.split(':') if ':' in message.text else [None, None]
    if (_hours and _minutes) and (_hours.isdigit() and _minutes.isdigit()):
        if 1 <= len(_hours) <= 2  and 1 <= len(_minutes) <= 2:
            if 0 <= int(_hours) <= 24 and 0 <= int(_minutes) <= 60:
                await bot_.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=(await state.get_data())['id'],
                    text=f'До будильника осталось ⏰\n\n'
                         f'{TimeManager(message.text).run_time_difference()}',
                    reply_markup=constructor_kb(cancel=True)
                )
                await state.clear()
                return
    await bot_.send_message()(
        chat_id=message.chat.id,
        text='Неверный формат❗️',
        reply_markup=constructor_kb(cancel=True)
    )
    await state.set_state(ClockState.alarm_clock_time)
# <--- /Clock State --->


# <--- Currency State --->
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
# <--- /Currency State --->

# <--- CheckIn State --->
class CheckInNameState(StatesGroup):
    check_in_name = State()

@router.message(CheckInNameState.check_in_name, F.text)
async def catch_check_in_name(message: Message, state: FSMContext):
    await bot_.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    async with CheckInMixin() as client:
        result1: dict = await client.create_check_in(
            check_in_name=message.text,
            user_id=message.from_user.id
        )

    async with CheckInMixin() as client:
        result2: dict = await client.get_all_user_check_in(
            user_id=message.from_user.id
        )

    _data = {item['check_in_name']: f"get_user_check_in#{item['id']}" for item in result2} if result2 else []
    _data['Создать check_in'] = 'create_check_in'

    await bot_.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data())['mess_id'],
        text=START_CHECK_IN_TEXT(result2),
        reply_markup=constructor_kb(
            data=_data,
            join=False,
            cancel=True
        )
    )

    await state.clear()
# <--- /CheckIn State --->