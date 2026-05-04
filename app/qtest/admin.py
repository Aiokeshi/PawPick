from django.contrib import admin

from .models import Answer, Question, TestResult, TestStep


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3
    fields = ('text', 'tag', 'order')
    ordering = ('order',)


@admin.register(TestStep)
class TestStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'weight')
    list_editable = ('order', 'weight')
    ordering = ('order',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'step', 'order')
    list_editable = ('step', 'order')
    list_filter = ('step',)
    ordering = ('step', 'order')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'tag', 'order')
    list_editable = ('order',)
    list_filter = ('question__step', 'tag__category')
    search_fields = ('text', 'question__text', 'tag__name')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'best_card', 'total_score', 'created_at')
    list_filter = ('created_at', 'best_card')
    readonly_fields = ('created_at',)
    filter_horizontal = ('tags', 'cards')
