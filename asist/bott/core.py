import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import DeleteWebhook

from os import getenv
from dotenv import load_dotenv


load_dotenv()

admin_id = [int(i) for i in getenv('ADMIN')[1:-1].split(', ')]
bot_ = Bot(
    token=getenv('TOKEN_API'),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)


async def on_startup(dispatcher):
    if admin_id:
        await bot_.send_message(
            chat_id=admin_id[0],
            text='Бот запущен!'
        )

async def on_shutdown(dispatcher):
    if admin_id:
        await bot_.send_message(
            chat_id=admin_id[0],
            text='Бот остановлен 😥'
        )

async def start_bot() -> None:
    await bot_(DeleteWebhook(drop_pending_updates=True))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await asyncio.gather(
        dp.start_polling(bot_)
    )