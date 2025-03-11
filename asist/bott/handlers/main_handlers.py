from asist.bott.core import router, bot_
from asist.bott.mixins.currency_mixin import CurrencyMixin
from asist.bott.mixins.finance_mixin import FinanceMixin
from asist.bott.mixins.check_in_mixin import CheckInMixin
from asist.bott.include import FSMContext, hbold, CallbackQuery, GREET_TEXT, pretty_courses_test, START_CHECK_IN_TEXT
from asist.bott.keyboards import constructor_kb, start_kb
from .states import ClockState


@router.callback_query(lambda query: query.data.startswith('main_menu'))
async def return_to_main_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=f'{GREET_TEXT[0]}\n\n{GREET_TEXT[-1]}',
        reply_markup=start_kb()
    )



@router.callback_query(lambda query: query.data.startswith('clock'))
async def get_time_before_alarm_clock(query: CallbackQuery, state: FSMContext):
    await state.clear()

    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    _msg_id = await bot_.send_message(
        chat_id=query.message.chat.id,
        text=hbold('Пришли мне время в формате "hh:mm"'),
        reply_markup=constructor_kb(cancel=True)
    )
    await state.set_data(
        {'id': _msg_id.message_id}
    )
    await state.set_state(ClockState.alarm_clock_time)



@router.callback_query(lambda query: query.data.startswith('currency'))
async def get_courses_of_currencies(query: CallbackQuery, state: FSMContext):
    await state.clear()

    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    async with CurrencyMixin() as session:
        await bot_.send_message(
            chat_id=query.message.chat.id,
            text=pretty_courses_test(await session.select_currency()),
            reply_markup=constructor_kb(
                data={
                    "Калькулятор 💎": "calculate"
                },
                cancel=True
            )
        )



@router.callback_query(lambda query: query.data.startswith('finances'))
async def get_finance_main_handler(query: CallbackQuery, state: FSMContext):
    await state.clear()

    async with FinanceMixin() as client:
        result = await client.get_all_user_finances(
            user_id=query.from_user.id
        )
    # await bot_.send_message(
    #     chat_id=query.message.chat.id,
    #     text=f'{GREET_TEXT[0]}\n\n{GREET_TEXT[-1]}',
    #     reply_markup=get_kb_with_scroll(get_chunk_buttons(data=result), int(idx))
    # )



@router.callback_query(lambda query: query.data.startswith('check_in'))
async def get_check_in_main_handler(query: CallbackQuery, state: FSMContext):
    await state.clear()

    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    async with CheckInMixin() as client:
        result: dict = await client.get_all_user_check_in(
            user_id=query.from_user.id
        )

    _data: dict = {item['check_in_name']: f"get_user_check_in#{item['id']}" for item in result} if result else {}
    _data['Создать check_in'] = 'create_check_in'

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=START_CHECK_IN_TEXT(result),
        reply_markup=constructor_kb(
            data=_data,
            join=False,
            cancel=True
        )
    )
