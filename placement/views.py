import json
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from questions.models import Question
from questions.serializers import QuestionSerializer
from curricula.models import Curriculum
from units.models import Unit


class PlacementTestView(TemplateView):
    template_name = 'placement_test.html'


# Receives get request, returns question packs for start and end skills of request scope (curriculum or unit) and pk
@api_view()
def initial_question_pack(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        start_pack = []
        end_pack = []
        start_skills_id_list = []
        end_skills_id_list = []
        if request.query_params["scope"] == "curriculum":
            curriculum = Curriculum.objects.get(id=request.query_params["pk"])
            start_skills_id_list.extend(json.loads(curriculum.start_skills)["skill_id_list"])
            end_skills_id_list.extend(json.loads(curriculum.end_skills)["skill_id_list"])
        elif request.query_params["scope"] == "currently_studying":
            curriculum = request.user.profile.currently_studying
            start_skills_id_list.extend(json.loads(curriculum.start_skills)["skill_id_list"])
            end_skills_id_list.extend(json.loads(curriculum.end_skills)["skill_id_list"])
        elif request.query_params["scope"] == "unit":
            unit = Unit.objects.get(id=request.query_params["pk"])
            start_skills_id_list.extend(json.loads(unit.start_skills)["skill_id_list"])
            end_skills_id_list.extend(json.loads(unit.end_skills)["skill_id_list"])
        else:
            raise ValidationError
        for i in start_skills_id_list:
            random_question = Question.objects.random(i)
            serialized_question = QuestionSerializer(random_question).data
            start_pack.append({"skill_id": i, "question": serialized_question})
        for i in end_skills_id_list:
            random_question = Question.objects.random(i)
            serialized_question = QuestionSerializer(random_question).data
            end_pack.append({"skill_id": i, "question": serialized_question})
        return Response({"start_skills_questions": start_pack, "end_skills_questions": end_pack, })

