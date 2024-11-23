from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок статьи",
        help_text="Введите заголовок")

    slug = models.CharField(
        max_length=100,
        verbose_name="slug",
        **NULLABLE
    )

    content = models.TextField(
        verbose_name='контент статьи',
        **NULLABLE
    )

    image = models.ImageField(
        upload_to="blog/image",
        verbose_name="Изображение",
        help_text="Загрузите изображение",
        **NULLABLE

    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )

    count_views = models.PositiveIntegerField(
        default=0,
        verbose_name='Просмотры',
        editable=False
    )

    owner = models.ForeignKey(
        User,
        verbose_name="Автор",
        help_text="Укажите автора внесения",
        **NULLABLE,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
