from django.contrib import admin
from .models import Skill, SkillEdge


class SkillEdgeInline(admin.TabularInline):
    model = SkillEdge
    fk_name = 'child_skill'
    extra = 1


class SkillAdmin(admin.ModelAdmin):
    model = Skill
    exclude = ('related_skills', )
    inlines = (SkillEdgeInline, )


class SkillEdgeAdmin(admin.ModelAdmin):
    model = SkillEdge


admin.site.register(Skill, SkillAdmin)
admin.site.register(SkillEdge, SkillEdgeAdmin)