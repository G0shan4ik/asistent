import asyncio

import sys
import logging

from asist.database import init
from asist.bott.core import start_bot

from loguru import logger


def start_dev() -> None:
    logger.success('Start APP')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    init()
    logger.info('<-- Init DB -->')
    try:
        logger.info('<-- Start BOT -->')
        asyncio.run(start_bot())
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        logger.warning('The bot was forcibly stopped')
