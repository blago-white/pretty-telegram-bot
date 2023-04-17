import asyncio
from typing import Union, Any

from ...config.pbconfig import *


async def start_delay(delay: int) -> None:
    """
    :param delay: delay in seconds

    start the async delay
    """

    if 0 < int(delay) < MAX_DELAY_TIME_SECONDS:
        await asyncio.sleep(delay=int(delay))


async def postpone_async_task(*tasks: list, delay: int) -> Any:
    """
    :param tasks: iterable object with asyncio futures
    :param delay: postpone time in seconds
    :return: result of coroutines
    """
    await start_delay(delay=int(delay))
    return [await task for task in tasks]
