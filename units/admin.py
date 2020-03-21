from django.contrib import admin
from .models import Unit


class UnitAdmin(admin.ModelAdmin):
    model = Unit
    exclude = ('slug', )


admin.site.register(Unit, UnitAdmin)
