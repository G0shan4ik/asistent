from aiogram.fsm.state import StatesGroup, State

from asist.bott.include import F, FSMContext, Message
from asist.bott.core import router, bot_
from asist.bott.keyboards import constructor_kb
from asist.bott.helpers import TimeManager


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