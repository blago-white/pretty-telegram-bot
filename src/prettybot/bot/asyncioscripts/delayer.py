import asyncio
from src.config.pbconfig import *


async def start_delay(delay: int) -> None:
    """
    :param delay: delay in seconds

    start the async delay
    """

    if 0 < int(delay) < MAX_DELAY_TIME_SECONDS:
        await asyncio.sleep(delay=int(delay))
