import contextlib
import dataclasses

import loguru
import typing
from tortoise import Tortoise

import vkquick
from src.models.user import DefaultClient
from src.utils import prepare_access_token
from vkquick.chatbot.wrappers.page import Page

from vkquick import TokenOwner

from settings import db_url, MODELS, ADMIN_TOKENS, TEST_MODE


@dataclasses.dataclass
class ConnectionClient:
    token_owner: TokenOwner
    owner_schema: Page
    token: str
    default_client: DefaultClient


async def generate_database() -> None:
    loguru.logger.critical("Database generated")
    await Tortoise.init(
        db_url=db_url,
        modules={'models': MODELS}
    )
    await Tortoise.generate_schemas()
    return None


# Генерация пользователей | Интеграция запуска.
async def generate_users() -> typing.AsyncIterator[ConnectionClient]:
    for admin_token in ADMIN_TOKENS:
        with contextlib.suppress(vkquick.APIError):
            _, user = await vkquick.API(prepare_access_token(admin_token)).define_token_owner()
            if user.is_user():
                client = await DefaultClient.filter(user_id=user.id).first()
                if not client:
                    client = await DefaultClient.create(user_id=user.id, access_token=prepare_access_token(admin_token),
                                                        permission=666)
                    await client.creating_other_dependencies_for_the_client()
                    if TEST_MODE:
                        loguru.logger.opt(colors=True).info("<blue>Test mode active</blue>")
                        yield ConnectionClient(token_owner=_,
                                               owner_schema=user,
                                               token=prepare_access_token(admin_token),
                                               default_client=client)

    if not TEST_MODE:
        async for default_client in DefaultClient.filter():
            with contextlib.suppress(vkquick.APIError):
                _, user = await vkquick.API(prepare_access_token(default_client.access_token)).define_token_owner()
                if user.is_user():
                    yield ConnectionClient(token_owner=_,
                                           owner_schema=user,
                                           token=prepare_access_token(default_client.access_token),
                                           default_client=default_client)
