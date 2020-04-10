from django.contrib import admin
from .models import Unit


class UnitAdmin(admin.ModelAdmin):
    model = Unit
    exclude = ('slug', )
    readonly_fields = ('start_skills', 'end_skills', 'subject')


admin.site.register(Unit, UnitAdmin)
