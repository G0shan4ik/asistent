import time
import asyncio
from functools import wraps

from .include import getenv, logger, load_dotenv

load_dotenv()


def timer(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if getenv("DEBUG", None):
            logger.info(f"Asynchronous function '{func.__name__}' completed for {elapsed_time:.4f} seconds.")

        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if getenv("DEBUG", None):
            logger.info(f"Synchronous function '{func.__name__}' completed for {elapsed_time:.4f} seconds.")

        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper