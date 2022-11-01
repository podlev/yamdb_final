from rest_framework import validators


def validate_username(value):
    """Проверка использования 'me' в качестве username"""
    if value == 'me':
        raise validators.ValidationError(
            "Использовать имя 'me' в качестве username запрещено."
        )
    return value
