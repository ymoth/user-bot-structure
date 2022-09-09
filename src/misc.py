import vkquick
from settings import PROJECT_NAME

from src.filters import PermissionFilter

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
