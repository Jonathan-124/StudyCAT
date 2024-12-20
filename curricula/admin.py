from django.contrib import admin
from .models import Curriculum


class CurriculumAdmin(admin.ModelAdmin):
    model = Curriculum
    exclude = ('slug', )
    readonly_fields = ('subject', 'start_skills', 'end_skills', 'prerequisite_skills')


admin.site.register(Curriculum, CurriculumAdmin)
