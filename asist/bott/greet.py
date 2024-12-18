from .texts import GREET_TEXT
from .commands import set_commands
from .keyboards import start_kb
from .core import dp
from .include import CommandStart, Message


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await set_commands()
    await message.answer(
        text=f'{GREET_TEXT[0]}\n\n\n{GREET_TEXT[-1]}',
        reply_markup=start_kb()
    )