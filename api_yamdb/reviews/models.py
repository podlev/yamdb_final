from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from reviews.validators import validate_year

User = get_user_model()


class Section(models.Model):
    """Модель, от которой будем наследовать модели Genre и Categories"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:settings.MAX_LENGTH]


class Categories(Section):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(Section):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField(validators=[validate_year])
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[:settings.MAX_LENGTH]


class GenreTitle(models.Model):
    """Вспомогательная модель жанров произведений"""
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, null=True)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)


class Review(models.Model):
    """Модель рейтинга произведений"""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comments(models.Model):
    """Модель комментариев к произведениям"""
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:settings.MAX_LENGTH]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
