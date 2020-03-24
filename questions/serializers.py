from rest_framework import serializers
from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('answer_text', 'answer_explanation', 'answer_correctness', 'answer_image')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_type', 'question_prompt', 'answers', 'prompt_image')
