from django.contrib import admin
from .models import Question, Answer, Image


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['pseudochance', 'discrimination']
    inlines = [
        AnswerInline,
    ]


class ImageAdmin(admin.ModelAdmin):
    model = Image


admin.site.register(Question, QuestionAdmin)
admin.site.register(Image, ImageAdmin)
