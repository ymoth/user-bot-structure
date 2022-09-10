import dataclasses
import typing

import vkquick

from vkquick.chatbot.dependency import Depends
from vkquick.chatbot.storages import NewMessage


@dataclasses.dataclass
class PermissionFilter(vkquick.BaseFilter):
    permission: int

    # Make decision handler check a user permission
    async def make_decision(self, ctx: NewMessage, **kwargs: Depends) -> None:
        from src.models.user import DefaultClient

        user = await DefaultClient.filter(user_id=ctx.msg.from_id).first()
        if not user or user.permission < self.permission or not ctx.msg.out:
            raise vkquick.StopCurrentHandling()
        return None

    # Получение команд, которые доступны пользователю
    def get_permission_commands(self) -> typing.List[vkquick.Command]:
        from src.misc import application

        commands: typing.List[vkquick.Command] = []
        for package in application.packages:
            # Проверка пакета <<application>>, если фильтр является нужным, пробегаемся по доступу.
            if isinstance(package.filter, PermissionFilter):
                if package.filter.permission == self.permission:
                    commands.extend([_command for _command in package.commands])
        return commands
