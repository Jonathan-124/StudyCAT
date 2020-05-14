from rest_framework import serializers
from .models import Curriculum


# Serializer for Curriculum objects
class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'
