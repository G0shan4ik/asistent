from aiogram.fsm.context import FSMContext

from asist.bott.core import bot_, router
from asist.bott.mixins.check_in_mixin import CheckInMixin
from asist.bott.include import START_CHECK_IN_TEXT, CallbackQuery
from asist.bott.keyboards import constructor_kb
from asist.bott.helpers import get_month_calendar, get_year_month, get_today_date, get_month_btn
from .states.check_in_state import CheckInNameState

from ast import literal_eval


@router.callback_query(lambda query: query.data.startswith('get_user_check_in#'))
async def catch_check_in(query: CallbackQuery):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    async with CheckInMixin() as client:
        result: dict = await client.get_check_in_by_id(
            check_in_id=query.data.split('#')[-1]
        )
        _data = {}
        year, month, check_in_dates = get_year_month(third_arg={})
        try:
            if result['dict_with_dates']:
                _data = literal_eval(result['dict_with_dates'])

                __test = _data[f'{year}#{month}']

                year, month, check_in_dates = get_year_month(third_arg=_data)
            else:
                _data[f'{year}#{month}'] = []

                await client.update_check_in(
                    check_in_id=int(query.data.split('#')[-1]),
                    data={
                        'dict_with_dates': f'{_data}'
                    }
                )
        except KeyError:
            _data[f'{year}#{month}'] = []

            await client.update_check_in(
                    check_in_id=int(query.data.split('#')[-1]),
                    data={
                        'dict_with_dates': f'{_data}'
                    }
                )

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=get_month_calendar(year=int(year), month=month, check_in_dates=check_in_dates),
        reply_markup=constructor_kb(
            data=get_month_btn(
                dct=_data,
                year=year,
                month=month,
                _check_in_id=int(query.data.split('#')[-1])
            ),
            join=False,
            num=2,
            cancel=True,
            prefix_cancel='check_in'
        )
    )


@router.callback_query(lambda query: query.data.startswith('create_check_in'))
async def create_check_in(query: CallbackQuery, state: FSMContext):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    msg = await bot_.send_message(
        chat_id=query.from_user.id,
        text='Введите название "check_in":'
    )

    await state.set_data({'mess_id': msg.message_id})

    await state.set_state(CheckInNameState.check_in_name)


@router.callback_query(lambda query: query.data.startswith('delete_check_in#'))
async def delete_check_in_first_step(query: CallbackQuery):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    await bot_.send_message(
        chat_id=query.message.chat.id,
        text='Вы уверены?',
        reply_markup=constructor_kb(
            data={
                'Да!': f'delete_check_in!#{query.data.split("#")[-1]}',
                'Нет!': f'get_user_check_in#{query.data.split("#")[-1]}',
            },
            num=2
        )
    )

@router.callback_query(lambda query: query.data.startswith('delete_check_in!#'))
async def delete_check_in_second_step(query: CallbackQuery):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    async with CheckInMixin() as client:
        result1: dict = await client.delete_check_in(
            check_in_id=query.data.split('#')[-1]
        )

    await query.answer(
        text='Успешно удалён!' if bool(result1['status']) else 'Что-то пошло не так...',
        show_alert=True
    )

    async with CheckInMixin() as client:
        result2: dict = await client.get_all_user_check_in(
            user_id=query.from_user.id
        )

    _data = {item['check_in_name']: f"get_user_check_in#{item['id']}" for item in result2} if result2 else []
    _data['Создать check_in'] = 'create_check_in'

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=START_CHECK_IN_TEXT(result2),
        reply_markup=constructor_kb(
            data=_data,
            join=False,
            cancel=True
        )
    )


@router.callback_query(lambda query: query.data.startswith('_check_in_'))
async def catch_check_in(query: CallbackQuery):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    res: bool = True if 'True' in query.data else False
    _check_in_id = int(query.data.split('#')[1])

    async with CheckInMixin() as client:
        result1: dict = await client.get_check_in_by_id(
            check_in_id=_check_in_id
        )
        if result1 and result1['dict_with_dates']:
            _data: dict = literal_eval(result1['dict_with_dates'])
            year, month, arr_with_dates = get_year_month(third_arg=_data)
            if res:
                if get_today_date() not in arr_with_dates:
                    arr_with_dates.append(get_today_date())
            else:
                if get_today_date() in arr_with_dates:
                    del arr_with_dates[arr_with_dates.index(get_today_date())]
            _data[f'{year}#{month}'] = arr_with_dates
        else:
            _data = {}
            year, month, arr_with_dates = get_year_month(third_arg=_data)
            if res:
                arr_with_dates = [get_today_date()]
                _data[f'{year}#{month}'] = arr_with_dates

        await client.update_check_in(
            check_in_id=_check_in_id,
            data={
                'dict_with_dates': f'{_data}'
            }
        )

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=get_month_calendar(year=int(year), month=month, check_in_dates=arr_with_dates),
        reply_markup=constructor_kb(
            data=get_month_btn(
                dct=literal_eval(result1['dict_with_dates']),
                year=year,
                month=month,
                _check_in_id=_check_in_id
            )
            ,
            join=False,
            num=2,
            cancel=True,
            prefix_cancel='check_in'
        )
    )


@router.callback_query(lambda query: query.data.startswith('skip#'))
async def skip_calendar(query: CallbackQuery):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    q_data = query.data.split('#')[1:]
    year, month, _check_in_id = q_data[0], q_data[1], int(q_data[2]),

    async with CheckInMixin() as client:
        result1: dict = await client.get_check_in_by_id(
            check_in_id=_check_in_id
        )

        _data: dict = literal_eval(result1['dict_with_dates'])

        arr_with_dates: list = _data[f'{year}#{month}']

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=get_month_calendar(year=int(year), month=month, check_in_dates=arr_with_dates),
        reply_markup=constructor_kb(
            data=get_month_btn(
                dct=literal_eval(result1['dict_with_dates']),
                year=int(year),
                month=month,
                _check_in_id=_check_in_id
            ),
            join=False,
            num=2,
            cancel=True,
            prefix_cancel='check_in'
        )
    )