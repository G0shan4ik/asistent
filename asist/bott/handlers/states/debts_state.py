from aiogram.fsm.state import StatesGroup, State

from asist.bott.include import (
    F, FSMContext, Message, CallbackQuery,
    CONSTRUCTOR_DEBT_INPUT_VALUE_TEXT, NO_DEBTS_TEXT,
    YES_DEBTS_TEXT, ERROR_SAVE_DEBT_TEXT, DEBT_SETTINGS_TEXT
)
from asist.bott.core import router, bot_
from asist.bott.keyboards import constructor_kb
from asist.bott.helpers import get_data_kb, check_valid_debt_data, calculate_due_date

from asist.bott.mixins.debts_mixin import DebtsMixin



class DebtsState(StatesGroup):
    wait_debt = State()
    catch_debt_message = State()
    catch_debt_query = State()


@router.callback_query(
    lambda query: query.data.startswith('save_debt'),
    DebtsState.wait_debt
)
async def save_debt(query: CallbackQuery, state: FSMContext):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    _data = await state.get_data()
    print('\n\n\n\n\n')
    print(_data)
    print('\n\n\n\n\n')
    if _data['update'][0]:
        _data = await state.get_data()
        prefix = _data.get('prefix_kb')
        debt_id = _data['update'][-1].split('#')[-1]
        request_data, flag = {}, {}

        async with DebtsMixin() as session:
            if prefix:
                for key, value in _data['request_data'].items():
                    request_data[key] = value

                flag: dict = await session.update_debts(debts_id=debt_id, data=request_data)

            data: dict = await session.get_debts_by_id(debts_id=debt_id)

        await query.answer(
            text='Изменения были добавлены !' if flag.get('status') else 'Изменения НЕ БЫЛИ обнаружены!',
            show_alert=True
        )
        await bot_.send_message(
            chat_id=query.message.chat.id,
            text=DEBT_SETTINGS_TEXT(data),
            reply_markup=constructor_kb(
                data={
                    f"Настройки ⚙️": f"debt_settings#{debt_id}",
                    f"Закрыть долг 🎊": f"close_debt#{debt_id}",
                },
                join=False,
                num=2,
                cancel=True,
                prefix_cancel='debts'
            )
        )

        await state.clear()
        return

    prefix = _data.get('prefix_kb')
    if prefix and 'title' in prefix and 'amount' in prefix:
        async with DebtsMixin() as session:
            request_data = {
                "user_id": query.message.chat.id
            }

            for key, value in _data['request_data'].items():
                request_data[key] = value

            data: dict = await session.create_debts(data=request_data)
            if data:
                data: list[dict] | list = await session.get_all_user_debts(user_id=query.message.chat.id)
                kb_data = {}
                if data:
                    for item in data:
                        for key, value in item.items():
                            if key == 'title':
                                kb_data[str(value)] = f'exists_debt#{item["id"]}'
                                break
                kb_data["Создать долг 💸"] = "create_debt"

                await bot_.send_message(
                    chat_id=query.message.chat.id,
                    text=YES_DEBTS_TEXT if data else NO_DEBTS_TEXT,
                    reply_markup=constructor_kb(
                        data=kb_data,
                        join=False,
                        cancel=True,
                    )
                )

                await state.clear()
                return

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=ERROR_SAVE_DEBT_TEXT,
        reply_markup=constructor_kb(
            data={},
            join=False,
            cancel=True,
            prefix_cancel='create_debt',
            name_cancel='Заполнить заново ↩️'
        )
    )
    await state.clear()


@router.callback_query(DebtsState.wait_debt)
async def catch_debt(query: CallbackQuery, state: FSMContext):
    # Хэндлю выход из 'Установки долга'
    if query.data == 'debts':
        await state.clear()

        await bot_.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )
        async with DebtsMixin() as session:
            data: list[dict] | list = await session.get_all_user_debts(user_id=query.message.chat.id)

        kb_data = {}
        if data:
            if data:
                for item in data:
                    for key, value in item.items():
                        if key == 'title':
                            kb_data[str(value)] = f'exists_debt#{item["id"]}'
                            break
        kb_data["Создать долг 💸"] = "create_debt"

        await bot_.send_message(
            chat_id=query.message.chat.id,
            text=YES_DEBTS_TEXT if data else NO_DEBTS_TEXT,
            reply_markup=constructor_kb(
                data=kb_data,
                join=False,
                cancel=True,
            )
        )
        return
    # Хэндлю выход из 'Обновления долга'
    elif query.data.startswith('exists_debt#'):
        await state.clear()

        await bot_.delete_message(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id
        )

        async with DebtsMixin() as session:
            data: dict = await session.get_debts_by_id(debts_id=query.data.split('#')[-1])

        debt_id = query.data.split('#')[-1]
        await bot_.send_message(
            chat_id=query.message.chat.id,
            text=DEBT_SETTINGS_TEXT(data),
            reply_markup=constructor_kb(
                data={
                    f"Настройки ⚙️": f"debt_settings#{debt_id}",
                    f"Закрыть долг 🎊": f"close_debt#{debt_id}",
                },
                join=False,
                num=2,
                cancel=True,
                prefix_cancel='debts'
            )
        )
        return

    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    _debt_state = query.data.split('#')[0]

    _data = await state.get_data()
    _data['current'] = _debt_state

    mess = await bot_.send_message(
        chat_id=query.message.chat.id,
        text=CONSTRUCTOR_DEBT_INPUT_VALUE_TEXT(_debt_state),
        reply_markup=constructor_kb(
            data=get_data_kb(_debt_state),
            join=False,
            num=3,
            cancel=True,
            prefix_cancel='create_debt' if not _data['update'][0] else f'debt_settings#{query.data.split("#")[-1]}'
        )
    )
    _data['mess_id'] = mess.message_id

    await state.set_data(_data)

    if _debt_state != 'priority':
        await state.set_state(DebtsState.catch_debt_message)
        return
    await state.set_state(DebtsState.catch_debt_query)


@router.message(DebtsState.catch_debt_message, F.text)
async def catch_debt_message(message: Message, state: FSMContext):
    await bot_.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    _data: dict = (await state.get_data())

    valid_or_no_data = check_valid_debt_data(
        debt_data=message.text,
        debt_state=_data['current']
    )
    if isinstance(valid_or_no_data, list):
        await bot_.edit_message_text(
            chat_id=message.chat.id,
            message_id=(await state.get_data())['mess_id'],
            text=valid_or_no_data[-1],
            reply_markup=constructor_kb(
                data={
                    'Назад ↩️':
                        (await state.get_data())['current'] if not _data.get('update') else f'title#update#{_data["update"][-1].replace("debt_settings#", "")}'
                },
                join=False,
                cancel=True,
                name_cancel='Вернуться в главное меню 🏠'
            )
        )

        await state.set_state(DebtsState.wait_debt)

        return

    if _data.get('request_data'):
        _data['request_data'][_data['current']] = message.text \
            if _data['current'] != 'due_date' \
            else calculate_due_date(debt_due_date=message.text)
    else:
        _data['request_data'] = {
            _data['current']: message.text \
                if _data['current'] != 'due_date' \
                else calculate_due_date(debt_due_date=message.text)
        }


    await bot_.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data())['mess_id'],
        text='Успешно сохранено !',
        reply_markup=constructor_kb(
            cancel=True,
            prefix_cancel='create_debt' if not _data["update"][0] else _data["update"][-1]
        )
    )

    if _data.get('prefix_kb'):
        _data['prefix_kb'].append(_data['current'])
    else:
        _data['prefix_kb'] = [_data['current']]

    await state.set_data(_data)


@router.callback_query(
    lambda query: query.data.startswith('priority#'),
    DebtsState.catch_debt_query)
async def catch_debt_query(query: CallbackQuery, state: FSMContext):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    _data: dict = (await state.get_data())

    if _data.get('prefix_kb'):
        _data['prefix_kb'].append(_data['current'])
    else:
        _data['prefix_kb'] = [_data['current']]

    if _data.get('request_data'):
        _data['request_data'][_data['current']] = query.data.replace('priority#', '')
    else:
        _data['request_data'] = {
            _data['current']: query.data.replace('priority#', '')
        }

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text='Успешно сохранено !',
        reply_markup=constructor_kb(
            cancel=True,
            prefix_cancel='create_debt' if not _data["update"][0] else _data["update"][-1]
        )
    )

    await state.set_data(_data)
