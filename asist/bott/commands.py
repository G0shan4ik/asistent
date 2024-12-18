from .core import bot_, Bot

from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot = bot_):
    commands = [
        BotCommand(
            command="start",
            description="Запустить бота"
        ),
        BotCommand(
            command="clock",
            description="Узнать время до будильника"
        ),
        BotCommand(
            command="courses_of_currencies",
            description="Актуальные курсы валют"
        )
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )