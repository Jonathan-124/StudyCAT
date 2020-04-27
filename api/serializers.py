from rest_framework import serializers


class PostTestUpdateSerializer(serializers.Serializer):
    score = serializers.DecimalField(4, 3, coerce_to_string=None, max_value=1, min_value=0)
    skill_pk = serializers.IntegerField()


class PostPlacementBulkUpdateSerializer(serializers.Serializer):
    confirmed_correct_skill_ids = serializers.ListField(child=serializers.IntegerField())
