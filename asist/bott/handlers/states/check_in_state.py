from aiogram.fsm.state import StatesGroup, State

from asist.bott.include import (
    F, FSMContext, Message,
    START_CHECK_IN_TEXT
)
from asist.bott.mixins.check_in_mixin import CheckInMixin
from asist.bott.core import router, bot_
from asist.bott.keyboards import constructor_kb


class CheckInNameState(StatesGroup):
    check_in_name = State()

@router.message(CheckInNameState.check_in_name, F.text)
async def catch_check_in_name(message: Message, state: FSMContext):
    await bot_.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    async with CheckInMixin() as client:
        await client.create_check_in(
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