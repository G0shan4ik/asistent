from .core import bot_, Bot

from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot = bot_):
    commands = [
        BotCommand(
            command="start",
            description="Главное меню."
        )
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )