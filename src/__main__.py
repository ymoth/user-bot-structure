"""
Code by https://github.com/ymoth
Igor Nezhivykh | 10.09.2022 0:53
"""

import asyncio

import loguru

from settings import ADMIN_TOKENS
from src.startup import generate_database
from src.startup import generate_users


async def success_running_program():
    if not ADMIN_TOKENS:
        loguru.logger.error("Append token to list: $settings.py:4")
        return

    await generate_database()

    async for default_client in generate_users():
        loguru.logger.opt(colors=True).critical(f"Connected client `{default_client.owner_schema.fullname}`")
        await default_client.default_client.coroutine_running()

# Coroutine running application with other dependencies
loop = asyncio.get_event_loop()
loop.create_task(success_running_program())
loop.run_forever()
