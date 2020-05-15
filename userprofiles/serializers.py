from rest_framework import serializers
from .models import CurrentlyStudying
from curricula.serializers import CurriculumSerializer


# Serializer for CurrentlyStudying objects
class CurrentlyStudyingSerializer(serializers.ModelSerializer):
    curriculum = CurriculumSerializer(read_only=True)

    class Meta:
        model = CurrentlyStudying
        exclude = ('user_profile', )
