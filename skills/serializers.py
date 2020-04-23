from rest_framework import serializers
from .models import Skill


# Serializer for Skill objects
class SkillSerializer(serializers.ModelSerializer):
    parent_ids = serializers.SerializerMethodField('get_parent_ids')
    child_ids = serializers.SerializerMethodField('get_child_ids')

    class Meta:
        model = Skill
        exclude = ('related_skills', )

    def get_parent_ids(self, obj):
        return obj.get_parent_skills().values_list('id', flat=True)

    def get_child_ids(self, obj):
        return obj.get_children_skills().values_list('id', flat=True)
