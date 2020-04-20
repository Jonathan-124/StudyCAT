from django.contrib import admin
from .models import UserProfile, Skillfulness, CurrentlyStudying


class SkillfulnessInline(admin.TabularInline):
    model = Skillfulness
    readonly_fields = ['skill']
    can_delete = False


class CurrentlyStudyingInline(admin.TabularInline):
    model = CurrentlyStudying


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    inlines = [
        SkillfulnessInline,
        CurrentlyStudyingInline
    ]
    can_delete = True


admin.site.register(UserProfile, UserProfileAdmin)
