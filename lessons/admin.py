from django.contrib import admin
from .models import Lesson


class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    exclude = ('slug', )


admin.site.register(Lesson, LessonAdmin)
