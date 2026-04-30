from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3  # сколько пустых полей показывать


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'step')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    filter_horizontal = ('tags',)