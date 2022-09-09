**user-bot-structure<br>
Логическое структурирование бота**

### Установка:
`git clone https://github.com/ymoth/user-bot-structure` <br>
Только для Python 3.10+
# Настройка
****

Основа сделана на PermissionFilter, в котором происходит проверка на пользователя
```py
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
    def get_permission_commands(self) -> list[vkquick.Command]:
        from src.misc import application

        commands: list[vkquick.Command] = []
        for package in application.packages:
            # Проверка пакета <<application>>, если фильтр является нужным, пробегаемся по доступу.
            if isinstance(package.filter, PermissionFilter):
                if package.filter.permission == self.permission:
                    commands.extend([_command for _command in package.commands])
        return commands

# src.misc
default_package = vkquick.Package(
    filter=PermissionFilter(0)
)

vip_package = vkquick.Package(
    filter=PermissionFilter(2)

)
agent_package = vkquick.Package(
    filter=PermissionFilter(3)
)

owner_package = vkquick.Package(
    filter=PermissionFilter(666)
)

# Главное приложение программы
application = vkquick.App(packages=[default_package, vip_package,
                                    agent_package, owner_package],
                          description="""
                          Ready-made structure, with ready-made functionality
                          and database implementation and migrations (tortoise-orm)
                          in the context of `settings.db_url`
                          """.replace(" " * 4, ""),
                          name=PROJECT_NAME)
```
Вся настройка хранится в settings.py
```py
PROJECT_NAME = "https://github.com/ymoth"
VERSION = "0.0.1"

ADMIN_TOKENS = []  # Токены могут быть в виде ссылки, регулярное выражение само берёт токен из ссылки

TEST_MODE = False  # Тест-мод, запуск администрации
MODELS = ["src.models.user"]  # Модели которые попадают интеграцию миграции базы данных и в саму инициализацию модели

default_string_time = "%d.%m.%Y %H:%M:%S"  # Обычное datetime.strftime для красивого выводы даты

db_url = "sqlite://src//models/users.sqlite"
# Documentation connecting MySQL and other https://tortoise-orm.readthedocs.io/en/latest/databases.html
```

# Миграция и база данных
***
База данных основана на `Tortoise-Object-Relational Mapping`;<br>
Все модели самой модели хранятся в src.models <br>
Миграция происходит через `aerich`, который уже готовый и настроен под изменения в базе данных.
```json
// src.models.migration
{
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": [*MODELS, "aerich.models"],
            "default_connection": "default",
        },
    },
}
```
Добавил/Удалил новую модель: <br>`aerich migrate --name edit_model ` <br> `aerich upgrade`

Использование самой ORM: https://tortoise-orm.readthedocs.io/en/latest/ <br>
Использование aerich: https://tortoise-orm.readthedocs.io/en/latest/migration.html

# Пакеты, `packages`
***
```commandline
Пакеты хранятся в директории src.sections.
Создание собственного пакета должно инициализироваться в sections.__init__.py для добавления хендлера

from . import default_package
from . import agent_package
from . import <your_package>
```

В самих пакетах должен быть `__init__.py` для того, что-бы команды устанавливались в пакеты.

# Запуск
***
Запуск происходит на основе `__main__.py` файла в директории src <br>
python3 -m src

Всё достаточно просто.