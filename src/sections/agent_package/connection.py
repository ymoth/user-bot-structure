import contextlib
import datetime
import typing

from settings import default_string_time

from src.models.user import DefaultClient
from src.message_handlers import error_text, success_text
from src.misc import agent_package
from src.utils import prepare_access_token

import vkquick


@agent_package.command("connect", "подключить", description="Подключает юзера. ")
async def create_new_client(context: vkquick.NewMessage, token: typing.Optional[str] = None) -> None:
    await context.msg.extend(context.api)
    access_token = prepare_access_token(token or context.msg.fields.get("reply_message", {}).get("text")
                                        or context.msg.fwd_messages[0].text)
    with contextlib.suppress(vkquick.APIError):
        _, prepare_the_client = await vkquick.API(access_token).define_token_owner()
        if prepare_the_client.is_user():
            if await DefaultClient.filter(user_id=prepare_the_client.id).first() is not None:
                await context.answer(f"Пользователь <<{prepare_the_client:@[fullname]}>> уже был ранее подключен. ")
                return
            client = await DefaultClient.create(
                user_id=prepare_the_client.id,
                permission=0,
                access_token=access_token,
                out_time_connection=datetime.datetime.now() + datetime.timedelta(days=30),
                update_connection=datetime.datetime.now()
            )
            await client.creating_other_dependencies_for_the_client()
            await client.coroutine_running()
            await context.answer(success_text(f"Отлично!\nПользователь {prepare_the_client:@[fullname]} был подключен "
                                              f"в {datetime.datetime.now().strftime(default_string_time)}"))
            return
    await context.answer(error_text("Ошибка VK-API | Обновите токен | https://vk.cc/cgbRts"))


@agent_package.command("update_token", "обновить", description="Обновляет юзера. ")
async def create_new_client(context: vkquick.NewMessage, token: typing.Optional[str] = None) -> None:
    await context.msg.extend(context.api)
    access_token = prepare_access_token(token or context.msg.reply_message.fields.get("text")
                                        or context.msg.fwd_messages[0].text)

    with contextlib.suppress(vkquick.APIError):
        _, prepare_the_client = await vkquick.API(access_token).define_token_owner()
        if prepare_the_client.is_user():
            if await DefaultClient.filter(user_id=prepare_the_client.id).first() is None:
                await context.answer(f"Пользователя <<{prepare_the_client:@[fullname]}>> не существует. ")
                return

            client = await DefaultClient.filter(user_id=prepare_the_client.id).first()
            client.update_connection = datetime.datetime.now()
            client.access_token = access_token
            await client.save()

            await client.coroutine_cancel()
            await client.coroutine_running()

            await context.answer(
                success_text(f"Отлично!\nПользователь {prepare_the_client:@[fullname]} был переподключен "
                             f"в {datetime.datetime.now().strftime(default_string_time)}")
            )
            return
    await context.answer(error_text("Ошибка VK-API | Обновите токен | https://vk.cc/cgbRts"))
