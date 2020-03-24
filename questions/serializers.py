from rest_framework import serializers
from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Answer
        fields = ('answer_text', 'answer_explanation', 'answer_correctness', 'image_url')

    def get_image_url(self, obj):
        if obj.answer_image:
            return obj.answer_image.url
        else:
            return ''


class QuestionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_type', 'question_prompt', 'answers', 'image_url')

    def get_image_url(self, obj):
        if obj.prompt_image:
            return obj.prompt_image.url
        else:
            return ''
