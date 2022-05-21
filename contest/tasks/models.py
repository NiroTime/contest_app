from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']


class Task(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )
    content = models.TextField(verbose_name='Описание задания')
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='tasks',
        verbose_name='Категория',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('task', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-time_create']
