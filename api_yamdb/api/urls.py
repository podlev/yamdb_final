from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, GenreViewSet,
                       TitlesViewSet, CommentsViewSet, ReviewViewSet)

v1_router = DefaultRouter()

v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentsViewSet, basename='comments')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
v1_router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
