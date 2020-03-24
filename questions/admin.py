from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['pseudochance', 'discrimination']
    inlines = [
        AnswerInline,
    ]


admin.site.register(Question, QuestionAdmin)
