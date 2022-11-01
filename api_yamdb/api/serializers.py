from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Title, Genre, Categories, Review, Comments
from reviews.validators import validate_year


class TitlesPostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title для записи данных"""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories"""

    class Meta:
        model = Categories
        exclude = ['id']
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title для чтения данных"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',
                  'rating')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, ser_data):
        """Проверяет, что к одному произведению можно поставить только один
        отзыв"""
        request = self.context.get('request')
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST'
                and Review.objects.filter(title=title,
                                          author=author).exists()):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв'
            )
        return ser_data

    class Meta:
        model = Review
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comments"""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
