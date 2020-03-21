from django.contrib import admin
from .models import Curriculum


class CurriculumAdmin(admin.ModelAdmin):
    model = Curriculum
    exclude = ('slug', )


admin.site.register(Curriculum, CurriculumAdmin)
