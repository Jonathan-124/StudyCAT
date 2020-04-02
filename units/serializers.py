from rest_framework import serializers
from .models import Unit
from lessons.serializers import LessonSerializer


class UnitSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ('name', 'slug', 'lessons')
