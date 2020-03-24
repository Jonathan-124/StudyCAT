from django.contrib import admin
from .models import Subject


class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    readonly_fields = ('dependencies', )


admin.site.register(Subject, SubjectAdmin)
