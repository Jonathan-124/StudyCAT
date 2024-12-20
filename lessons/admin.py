from django.contrib import admin
from .models import Lesson, LessonImage


class LessonImageInline(admin.TabularInline):
    model = LessonImage


class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    inlines = (LessonImageInline, )
    exclude = ('slug', )
    ordering = ('lesson_title', )


admin.site.register(Lesson, LessonAdmin)
