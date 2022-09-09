import time

import vkquick
from src.message_handlers import success_text

from src.misc import default_package

from settings import default_string_time


@default_package.command("ping", "пинг")
async def prepare_ping(context: vkquick.NewMessage) -> None:
    await context.edit(success_text(f"Context eventing by: {context.msg.date.now().strftime(default_string_time)}\n"
                                    f"Eventing time: {abs(round(time.time() - context.msg.date.timestamp(), 4))} seconds. "))
