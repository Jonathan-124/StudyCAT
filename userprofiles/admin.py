from django.contrib import admin
from .models import UserProfile, Skillfulness


class SkillfulnessInline(admin.TabularInline):
    model = Skillfulness
    readonly_fields = ['skill']


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        SkillfulnessInline,
    ]


admin.site.register(UserProfile, UserProfileAdmin)
