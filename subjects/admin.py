from django.contrib import admin
from .models import Subject


class SubjectAdmin(admin.ModelAdmin):
    model = Subject


admin.site.register(Subject, SubjectAdmin)
