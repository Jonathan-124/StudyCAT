from django.contrib import admin
from .models import QuestionBugReport, GeneralBugReport


class QuestionBugReportAdmin(admin.ModelAdmin):
    readonly_fields = ['reporting_user', 'question', 'reason', 'report_message']


class GeneralBugReportAdmin(admin.ModelAdmin):
    readonly_fields = ['reporting_user', 'report_message']


admin.site.register(QuestionBugReport, QuestionBugReportAdmin)
admin.site.register(GeneralBugReport, GeneralBugReportAdmin)
