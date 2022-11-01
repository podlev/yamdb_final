from django.core.exceptions import ValidationError
import datetime as dt


def validate_year(value):
    """Проверка, что год не превышает текущий"""
    year = dt.date.today().year
    if not value <= year:
        raise ValidationError(
            'Проверьте год издания произведения!')
    return value
