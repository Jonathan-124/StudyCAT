from rest_framework import serializers
from .models import GeneralBugReport, QuestionBugReport


# Serializer for GeneralBugReport objects
class GeneralBugReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralBugReport
        exclude = ()

    def create(self, validated_data):
        # Appends reporting_user field when validating bug report post request
        if 'reporting_user' not in validated_data:
            validated_data['reporting_user'] = self.context['request'].user
        return GeneralBugReport.objects.create(**validated_data)


# Serializer for QuestionBugReport objects
class QuestionBugReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionBugReport
        exclude = ()

    def create(self, validated_data):
        # Appends reporting_user field when validating bug report post request
        if 'reporting_user' not in validated_data:
            validated_data['reporting_user'] = self.context['request'].user
        return QuestionBugReport.objects.create(**validated_data)
