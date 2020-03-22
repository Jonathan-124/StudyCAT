from django.views.generic import DetailView
from .models import Curriculum
from skills.models import Skill
from questions.serializers import QuestionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


class CurriculumView(DetailView):
    model = Curriculum
    template_name = "curriculum.html"


# Receives get request, returns question packs for start and end skills of user indicated currently_studying curriculum
@api_view()
def get_placement_initial_question_pack(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        curriculum = user_profile.currently_studying
        start_skills_id_list = json.loads(curriculum.start_skills)["skill_id_list"]
        end_skills_id_list = json.loads(curriculum.end_skills)["skill_id_list"]
        start_pack = []
        end_pack = []
        for i in start_skills_id_list:
            random_question = Skill.objects.get(id=i).questions.random()
            serialized_question = QuestionSerializer(random_question).data
            start_pack.append({"skill_id": i, "question": serialized_question})
        for i in end_skills_id_list:
            random_question = Skill.objects.get(id=i).questions.random()
            serialized_question = QuestionSerializer(random_question).data
            end_pack.append({"skill_id": i, "question": serialized_question})
        return Response({"start_skills_questions": start_pack, "end_skills_questions": end_pack, })
