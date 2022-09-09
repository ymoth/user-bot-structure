from settings import db_url, MODELS

# Структура для миграции базы данных.
structure = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": [*MODELS, "aerich.models"],
            "default_connection": "default",
        },
    },
}
