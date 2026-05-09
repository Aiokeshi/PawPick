from django.conf import settings
from django.db import models


class TagCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория тегов'
        verbose_name_plural = 'Категории тегов'

    def __str__(self):
        return self.name


class Tag(models.Model):
    category = models.ForeignKey(
        TagCategory,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=100, verbose_name='Тег')

    class Meta:
        unique_together = ('category', 'name')
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.category.name}: {self.name}'


class Cards(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URl')
    height = models.TextField(blank=True, null=True, verbose_name='Рост')
    weight = models.TextField(blank=True, null=True, verbose_name='Вес')
    age = models.TextField(blank=True, null=True, verbose_name='Продолжительность жизни')
    furrColors = models.TextField(blank=True, null=True, verbose_name='Окрасы')
    imageMain = models.ImageField(upload_to='card_images', blank=True, null=True, verbose_name='Главное изображение')
    imageScnd = models.ImageField(upload_to='card_images', blank=True, null=True, verbose_name='Изображение')
    imageThrd = models.ImageField(upload_to='card_images', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    health = models.TextField(blank=True, null=True, verbose_name='Здоровье')

    tags = models.ManyToManyField(
        Tag,
        related_name='cards',
        blank=True,
        verbose_name='Теги'
    )

    class Meta:
        db_table = 'card'
        verbose_name = 'Карточки'
        verbose_name_plural = 'Карта'

    def __str__(self):
        return self.name


class FavoriteCard(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_cards',
        verbose_name='Пользователь'
    )
    card = models.ForeignKey(
        Cards,
        on_delete=models.CASCADE,
        related_name='favorite_users',
        verbose_name='Карточка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Избранная карточка'
        verbose_name_plural = 'Избранные карточки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'card'],
                name='unique_user_favorite_card'
            )
        ]

    def __str__(self):
        return f'{self.user}: {self.card}'
