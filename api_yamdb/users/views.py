from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .permissions import IsAdmin
from .serializers import (UserSerializer,
                          TokenSerializer, RegistrationSerializer)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdmin)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'PATCH':
            user = request.user
            serializer = UserSerializer(user, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['role'] = user.role
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def new_user(request):
    """Функция создания нового пользователя"""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    email = request.data.get('email')
    try:
        user, _ = User.objects.get_or_create(**serializer.validated_data)
    except IntegrityError:
        raise ValidationError(
            'A user with that username or email is already exists')
    try:
        send_mail(
            subject='New registration',
            recipient_list=[email],
            message=f'Your code: {default_token_generator.make_token(user)}',
            from_email=settings.EMAIL,
            fail_silently=False
        )
    except SMTPException as e:
        return Response({'error': e},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'username': username, 'email': email},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def update_token(request):
    """Функция получения токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response({'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'invalid code'},
                    status=status.HTTP_400_BAD_REQUEST)
