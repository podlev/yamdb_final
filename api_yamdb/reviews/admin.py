from django.contrib import admin
from reviews.models import Categories, Genre, Title, Review, Comments
from users.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year',)
    search_fields = ('name',)
    list_filter = ('category__slug', 'year',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(Categories, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comments)
