from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Genre, Title, Review
from users.permissions import (IsAdminOrReadOnly,
                               IsReadOnlyOrIsAuthorOrIsModerator)

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (CategoriesSerializer,
                          GenreSerializer,
                          TitlesSerializer,
                          TitlesPostSerializer,
                          CommentsSerializer,
                          ReviewSerializer)


class CategoriesViewSet(ListCreateDestroyViewSet):
    """Представление для категорий произведений"""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """Представление для жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    filter_class = TitleFilter
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """Представление для произведений"""
    pagination_class = LimitOffsetPagination
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Переопределение выбора сериализатора"""
        if self.action in ('retrieve', 'list'):
            return TitlesSerializer
        return TitlesPostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов на произведения"""
    serializer_class = ReviewSerializer
    permission_classes = (IsReadOnlyOrIsAuthorOrIsModerator,)

    def get_queryset(self):
        """Переопределение queryset"""""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение метода create"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Представление для комментариев к отзывам"""
    serializer_class = CommentsSerializer
    permission_classes = (IsReadOnlyOrIsAuthorOrIsModerator,)

    def get_queryset(self):
        """Переопределение queryset"""""
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title__id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Переопределение метода create"""
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
