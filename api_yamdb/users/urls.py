from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, new_user, update_token

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('users/<str:username>/', UserViewSet)

urlpatterns = [
    path('api/v1/', include(v1_router.urls)),
    path('api/v1/auth/signup/', new_user),
    path('api/v1/auth/token/', update_token)
]
