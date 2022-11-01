from django.conf import settings
from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework import serializers

from .models import User
from .validators import validate_username


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации"""

    username = serializers.CharField(max_length=settings.MAX_USERNAME_LENGTH,
                                     validators=[ASCIIUsernameValidator,
                                                 validate_username])
    email = serializers.EmailField()


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена"""
    username = serializers.CharField(max_length=settings.MAX_USERNAME_LENGTH)
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта /api/v1/users"""

    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
