from django.contrib.auth.models import User
from django.db import models

from catalog.models import Cards, Tag


class TestStep(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название шага')
    order = models.PositiveIntegerField(unique=True, verbose_name='Порядок')
    weight = models.PositiveIntegerField(default=1, verbose_name='Вес шага')

    class Meta:
        ordering = ['order']
        verbose_name = 'Шаг теста'
        verbose_name_plural = 'Шаги теста'

    def __str__(self):
        return f'{self.order}. {self.title}'


class Question(models.Model):
    text = models.CharField(max_length=255, verbose_name='Вопрос')
    step = models.PositiveIntegerField(verbose_name='Номер шага')
    order = models.PositiveIntegerField(default=1, verbose_name='Порядок внутри шага')

    class Meta:
        ordering = ['step', 'order']
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы теста'

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    text = models.CharField(max_length=255, verbose_name='Ответ')
    tag = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        related_name='answers',
        null=True,
        blank=True,
        verbose_name='Тег ответа'
    )
    order = models.PositiveIntegerField(default=1, verbose_name='Порядок')

    class Meta:
        ordering = ['question__step', 'question__order', 'order']
        verbose_name = 'Ответ теста'
        verbose_name_plural = 'Ответы теста'

    def __str__(self):
        return self.text


class TestResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Полученные теги')
    cards = models.ManyToManyField(Cards, blank=True, verbose_name='Карточки результата')
    best_card = models.ForeignKey(
        Cards,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='best_results',
        verbose_name='Лучший результат'
    )
    total_score = models.PositiveIntegerField(default=0, verbose_name='Итоговые баллы')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты теста'

    def __str__(self):
        return f'Result {self.id}'
