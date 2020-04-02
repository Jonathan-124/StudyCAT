from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    topological_order = serializers.SerializerMethodField('get_topological_order')

    class Meta:
        model = Lesson
        fields = ('lesson_title', 'slug', 'topological_order')

    def get_topological_order(self, obj):
        return obj.skill.topological_order
