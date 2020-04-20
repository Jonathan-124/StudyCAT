from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['question_prompt', 'question_type', 'skill']
    list_filter = ['skill']
    readonly_fields = ['pseudochance', 'discrimination']
    inlines = [
        AnswerInline,
    ]


admin.site.register(Question, QuestionAdmin)
