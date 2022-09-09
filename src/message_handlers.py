from settings import PROJECT_NAME

default_new_line = "\n"


def default_text(message: str, new_line: str = default_new_line) -> str:
    return f"✨ | {PROJECT_NAME}{new_line}{message}"


def error_text(message: str, new_line: str = default_new_line) -> str:
    return f"❗ | {PROJECT_NAME}{new_line}{message}"


def success_text(message: str, new_line: str = default_new_line) -> str:
    return f"✅ | {PROJECT_NAME}{new_line}{message}"


def warning_text(message: str, new_line: str = default_new_line) -> str:
    return f"⚠ | {PROJECT_NAME}{new_line}{message}"
