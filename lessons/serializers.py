from rest_framework import serializers
from .models import Lesson
from skills.serializers import SkillSerializer


class LessonSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(many=False, read_only=True)

    class Meta:
        model = Lesson
        fields = ('lesson_title', 'slug', 'skill')
