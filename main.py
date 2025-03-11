import asyncio

import sys
import logging
from loguru import logger

from asist.bott.core import run_bot
from asist.api.core import run_api

from os import getenv


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    api_task = asyncio  .create_task(run_api())
    bot_task = asyncio.create_task(run_bot())

    await asyncio.gather(api_task, bot_task, return_exceptions=True)

def start_dev() -> None:
    logger.success('Starting application...')

    if getenv("DEBUG", False):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Application was stopped')
