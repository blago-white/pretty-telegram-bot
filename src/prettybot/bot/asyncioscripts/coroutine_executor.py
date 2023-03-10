import asyncio


async def execute_coros(*coroutines):
    return await asyncio.gather(*[asyncio.create_task(task) for task in coroutines])
