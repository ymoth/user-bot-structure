import asyncio
import contextlib
import typing

import tortoise

from src.misc import application


# Client settings by <USER_ID> argument
class ClientSettings(tortoise.Model):
    user_id = tortoise.fields.IntField(unique=True)
    prefixes = tortoise.fields.JSONField(default=["!", ".м "])

    statistics = tortoise.fields.JSONField(default={
        "used_commands": [{"name": "null", "utctime": 0}],
        "games": {}
    })

    quote_setting = tortoise.fields.TextField(default="black")

    class Meta:
        table = "clientSettings"


class DefaultClient(tortoise.Model):
    id = tortoise.fields.IntField(pk=True)
    user_id = tortoise.fields.IntField(unique=True)

    permission = tortoise.fields.IntField(default=0)
    access_token = tortoise.fields.CharField(max_length=198)

    created_user = tortoise.fields.DatetimeField(auto_now_add=True)
    nickname = tortoise.fields.CharField(max_length=60, default="MultiLilite best.")

    out_time_connection = tortoise.fields.DatetimeField(null=True)
    update_connection = tortoise.fields.DatetimeField(null=True)

    async def get_settings(self) -> ClientSettings:
        return await ClientSettings.filter(user_id=self.user_id).first()

    # Создание зависимостей для клиента, создаются указанные модели.
    async def creating_other_dependencies_for_the_client(self) -> ClientSettings:
        settings = await ClientSettings.create(user_id=self.user_id)
        return settings

    async def coroutine_running(self) -> None:
        asyncio.create_task(application.coroutine_run(self.access_token, build_autodoc=False), name=str(self.user_id))
        return None

    async def coroutine_cancel(self) -> bool:
        with contextlib.suppress(asyncio.CancelledError):
            for default_task in asyncio.all_tasks():
                if default_task.get_name().__eq__(str(self.user_id)):
                    default_task.cancel()
                    return True
        return False

    class Meta:
        table = "defaultClient"
