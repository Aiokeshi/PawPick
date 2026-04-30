from django.db import models
from catalog.models import Tag, Cards
from django.contrib.auth.models import User


class Question(models.Model):
    text = models.CharField(max_length=255)
    step = models.IntegerField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    text = models.CharField(max_length=255)

    tags = models.ManyToManyField(
        Tag,
        related_name='answers'  # ВАЖНО
    )

    def __str__(self):
        return self.text
    
class TestResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag)
    cards = models.ManyToManyField(Cards)

    best_card = models.ForeignKey(
        Cards,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='best_results'
    )

    def __str__(self):
        return f"Result {self.id}"
    

    