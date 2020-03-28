from rest_framework import serializers
from .models import GeneralBugReport, QuestionBugReport


class GeneralBugReportSerializer(serializers.ModelSerializer):
    reporting_user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = GeneralBugReport
        exclude = ()


class QuestionBugReportSerializer(serializers.ModelSerializer):
    reporting_user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = QuestionBugReport
        exclude = ()
