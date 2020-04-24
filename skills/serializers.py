from rest_framework import serializers
from .models import Skill


# Serializer for Skill objects
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ('related_skills', )
