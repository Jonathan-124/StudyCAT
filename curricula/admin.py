from django.contrib import admin
from .models import Curriculum


class CurriculumAdmin(admin.ModelAdmin):
    model = Curriculum
    exclude = ('slug', )
    readonly_fields = ('start_skills', 'end_skills')


admin.site.register(Curriculum, CurriculumAdmin)
