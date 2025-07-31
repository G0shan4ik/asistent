from asist.bott.core import router, bot_
from asist.bott.mixins.debts_mixin import DebtsMixin
from asist.bott.include import (
    FSMContext, CallbackQuery,
    NO_DEBTS_TEXT, START_CREATE_DEBTS_TEXT, YES_DEBTS_TEXT, DELETE_DEBT_TEXT, DEBT_SETTINGS_TEXT, UPDATE_DEBTS_TEXT
)
from asist.bott.keyboards import constructor_kb
from .states.debts_state import DebtsState


@router.callback_query(lambda query: query.data.startswith('debts'))
async def return_calculate_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()

    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    async with DebtsMixin() as session:
        data: dict = await session.get_all_user_debts(user_id=query.message.chat.id)

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


@router.callback_query(lambda query: query.data.startswith('create_debt'))
async def return_create_debt_menu(query: CallbackQuery, state: FSMContext):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    _data = await state.get_data()
    prefix_kb = _data.get('prefix_kb')
    _data['update'] = [False, '']
    await state.set_data(_data)

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=START_CREATE_DEBTS_TEXT,
        reply_markup=constructor_kb(
            data={
                f"Название{' ✅' if prefix_kb and 'title' in prefix_kb else ''}": "title",
                f"Сумма{' ✅' if prefix_kb and 'amount' in prefix_kb else ''}": "amount",
                f"Приоритет{' ✅' if prefix_kb and 'priority' in prefix_kb else ''}": "priority",
                f"Срок выплаты{' ✅' if prefix_kb and 'due_date' in prefix_kb else ''}": "due_date",
                f"Сохранить ☑️": "save_debt",
            },
            join=False,
            num=2,
            cancel=True,
            prefix_cancel='debts'
        )
    )

    await state.set_state(DebtsState.wait_debt)


@router.callback_query(lambda query: query.data.startswith('exists_debt#'))
async def return_create_debt_menu(query: CallbackQuery, state: FSMContext):
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


@router.callback_query(lambda query: query.data.startswith('close_debt#'))
async def return_create_debt_menu(query: CallbackQuery, state: FSMContext):
    await state.clear()

    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    async with DebtsMixin() as session:
        data: dict = await session.delete_debts(debts_id=query.data.split('#')[-1])

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=DELETE_DEBT_TEXT(data),
        reply_markup=constructor_kb(
            join=False,
            cancel=True,
            name_cancel='Вернуться в главное меню 🏠'
        )
    )


@router.callback_query(lambda query: query.data.startswith('debt_settings#'))
async def return_create_debt_menu(query: CallbackQuery, state: FSMContext):
    await bot_.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )
    _data = await state.get_data()
    prefix_kb = _data.get('prefix_kb')
    _data['update'] = [True, f'debt_settings#{query.data.split("#")[-1]}']
    await state.set_data(_data)

    await bot_.send_message(
        chat_id=query.message.chat.id,
        text=UPDATE_DEBTS_TEXT,
        reply_markup=constructor_kb(
            data={
                f"Название{' ✅' if prefix_kb and 'title' in prefix_kb else ''}": f"title#update#{query.data.split('#')[-1]}",
                f"Сумма{' ✅' if prefix_kb and 'amount' in prefix_kb else ''}": f"amount#update#{query.data.split('#')[-1]}",
                f"Приоритет{' ✅' if prefix_kb and 'priority' in prefix_kb else ''}": f"priority#update#{query.data.split('#')[-1]}",
                f"Погасить часть{' ✅' if prefix_kb and 'paid' in prefix_kb else ''}": f"paid#update#{query.data.split('#')[-1]}",
                f"Срок выплаты{' ✅' if prefix_kb and 'due_date' in prefix_kb else ''}": f"due_date#update#{query.data.split('#')[-1]}",
                f"Примечание{' ✅' if prefix_kb and 'notes' in prefix_kb else ''}": f"notes#update#{query.data.split('#')[-1]}",
                f"Сохранить ☑️": f"save_debt",
            },
            join=False,
            cancel=True,
            num=2,
            prefix_cancel=f'exists_debt#{query.data.split("#")[-1]}'
        )
    )

    await state.set_state(DebtsState.wait_debt)