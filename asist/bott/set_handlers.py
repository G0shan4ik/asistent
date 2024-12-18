from .core import router
from .states import ClockState
from .include import Command, Message, FSMContext, F, hbold
from .keyboards import cancel_kb
from asist.parser.pars_course_currencies import update_courses


@router.message(Command(commands=['clock']))
async def get_time_before_alarm_clock(message: Message, state: FSMContext):
    await message.answer(
        text=hbold('Пришли мне время в формате "hh:mm"'),
        reply_markup=cancel_kb()
    )
    await state.set_state(ClockState.alarm_clock_time)


@router.message(Command(commands=['courses_of_currencies']))
async def get_time_before_alarm_clock(message: Message, state: FSMContext):
    data = await update_courses()
    print(data)
    await message.answer('courses_of_currencies')

@router.message(F.text == "Финансы💸")
async def finance_module(message: Message):
    await message.answer('Финансы💸')

@router.message(F.text == "Мои планы🌵")
async def plans_module(message: Message):
    data = await update_courses()
    print(data)
    await message.answer('Мои планы🌵')