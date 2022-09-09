import re
import time

import vkquick

from src.misc import default_package
from src.misc import vip_package
from src.misc import agent_package
from src.misc import owner_package

from src.models.user import DefaultClient


# Получение токена из <<string_object>> | regex: (vk1[A-Za-z0-9_,-.]+|[a-f\d]{85})
def prepare_access_token(string_object: str) -> str | None:
    return re.search(r"(vk1[A-Za-z0-9_,-.]+|[a-f\d]{85})", string_object).group(0)


# Постановка статистики пользователя
async def set_statistics_user(context: vkquick.NewMessage, user: DefaultClient) -> None:
    statistic_ignore_commands, settings = ["стата", "инфо", "профиль"], await user.get_settings()
    for prefix in settings.prefixes:
        if context.msg.text.lower().startswith(prefix):
            command_prepare = context.msg.text.lower().replace(prefix, "").split()
            if command_prepare[0] not in statistic_ignore_commands:
                settings.statistics["used_commands"].append({"name": command_prepare[0], "utctime": time.time(),
                                                             "arguments": command_prepare})
                await settings.save()
                return None
    return None


# Кастомная обработка сообщений после дефолтного обработчика команды.
async def process_after_message_handle_is_complete(context: vkquick.NewMessage) -> None:
    client: DefaultClient = await DefaultClient.filter(user_id=context.msg.from_id).first()
    await set_statistics_user(context=context, user=client)
    return None


# Конструктор привилегий с n-аргументами.
permission_construct = {
    0: {"name": "Пользователь", "price": 100, "emoji": "⭐", "package_commands": default_package.commands},
    10: {"name": "Вип", "price": 50, "emoji": "🍀", "package_commands": vip_package.commands},
    50: {"name": "Агент", "price": 0, "emoji": "⚠", "package_commands": agent_package.commands},
    666: {"name": "Создатель", "price": 0, "emoji": "👤", "package_commands": owner_package.commands}
}
