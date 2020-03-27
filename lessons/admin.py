from django.contrib import admin
from .models import Lesson, LessonImage


class LessonImageInline(admin.TabularInline):
    model = LessonImage


class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    inlines = (LessonImageInline, )
    exclude = ('slug', )


admin.site.register(Lesson, LessonAdmin)
