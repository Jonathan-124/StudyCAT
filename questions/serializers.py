from rest_framework import serializers
from .models import Question, Answer


# Serializer for Answer objects
class AnswerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Answer
        fields = ('answer_text', 'answer_explanation', 'answer_correctness', 'image_url')

    # populates image_url field if answer object has a non-empty image field
    def get_image_url(self, obj):
        if obj.answer_image:
            return obj.answer_image.url
        else:
            return ''


# Serializer for Question objects, includes associated answers' serialized objects
class QuestionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'skill', 'question_type', 'question_prompt', 'answers', 'image_url', 'permitted_symbols')

    # populates image_url field if question object has a non-empty image field
    def get_image_url(self, obj):
        if obj.prompt_image:
            return obj.prompt_image.url
        else:
            return ''
