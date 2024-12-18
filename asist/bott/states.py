from aiogram.fsm.state import StatesGroup, State

from .include import F, FSMContext, Message
from .core import router
from .keyboards import start_kb
from .helpers import time_difference, time_to_text


class ClockState(StatesGroup):
    alarm_clock_time = State()


@router.message(F.text == 'Отмена')  # exit the state
async def exit_the_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вурнулись в главное меню.',
        reply_markup=start_kb()
    )
    await state.clear()


@router.message(ClockState.alarm_clock_time, F.text)
async def catch_time(message: Message, state: FSMContext):
    _hours, _minutes = message.text.split(':') if ':' in message.text else [None, None]
    if (_hours and _minutes) and (_hours.isdigit() and _minutes.isdigit()):
        if 1 <= len(_hours) <= 2  and 1 <= len(_minutes) <= 2:
            if 0 <= int(_hours) <= 24 and 0 <= int(_minutes) <= 60:
                await message.answer(
                    text=f'До будильника осталось ⏰\n\n'
                         f'{time_to_text(time_difference(message.text))}',
                    reply_markup=start_kb()
                )
                await state.clear()
                return
    await message.answer('Неверный формат❗️')
    await state.set_state(ClockState.alarm_clock_time)

