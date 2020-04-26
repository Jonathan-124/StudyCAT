from rest_framework import serializers
from .models import GeneralBugReport, QuestionBugReport, LessonBugReport, UnitBugReport, CurriculumBugReport


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


class LessonBugReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonBugReport
        exclude = ()

    def create(self, validated_data):
        # Appends reporting_user field when validating bug report post request
        if 'reporting_user' not in validated_data:
            validated_data['reporting_user'] = self.context['request'].user
        return LessonBugReport.objects.create(**validated_data)


class UnitBugReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitBugReport
        exclude = ()

    def create(self, validated_data):
        # Appends reporting_user field when validating bug report post request
        if 'reporting_user' not in validated_data:
            validated_data['reporting_user'] = self.context['request'].user
        return UnitBugReport.objects.create(**validated_data)


class CurriculumBugReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurriculumBugReport
        exclude = ()

    def create(self, validated_data):
        # Appends reporting_user field when validating bug report post request
        if 'reporting_user' not in validated_data:
            validated_data['reporting_user'] = self.context['request'].user
        return CurriculumBugReport.objects.create(**validated_data)