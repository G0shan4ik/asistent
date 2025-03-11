from .texts import GREET_TEXT, WRONG_TEXT
from .commands import set_commands
from .keyboards import start_kb
from .core import dp, bot_, admin_id
from .include import CommandStart, Message, UserMixin


@dp.message(CommandStart())
async def start_cmd(message: Message):
    if message.from_user.id not in admin_id:
        await message.answer(
            text='Sorry, You not admin('
        )
        return

    await set_commands()
    await message.delete()
    async with UserMixin() as client:
        result = await client.create_user(
            user_id=message.from_user.id,
            user_name=message.from_user.username
        )
        if result['created_id']:
            await bot_.send_message(
                chat_id=message.chat.id,
                text=f'{GREET_TEXT[0]}\n\n{GREET_TEXT[-1]}',
                reply_markup=start_kb()
            )
            return
        await bot_.send_message(
            chat_id=message.chat.id,
            text=WRONG_TEXT
        )