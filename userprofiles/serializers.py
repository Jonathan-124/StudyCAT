from rest_framework import serializers
from .models import CurrentlyStudying
from curricula.serializers import CurriculumSerializer


# Serializer for CurrentlyStudying objects
class CurrentlyStudyingSerializer(serializers.ModelSerializer):
    curriculum = CurriculumSerializer(read_only=True)

    class Meta:
        model = CurrentlyStudying
        exclude = ('user_profile', )

    def validate(self, data):
        if CurrentlyStudying.objects.exists(curriculum__id=self.context['request'].user.profile.data['curriculum']):
            raise serializers.ValidationError('User is already studying for this course')
        return data

    def create(self, validated_data):
        if 'user_profile' not in validated_data:
            validated_data['user_profile'] = self.context['request'].user.profile
        return CurrentlyStudying.objects.create(**validated_data)
