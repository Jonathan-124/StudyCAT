from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import UserProfilePretestForm
from .models import Skillfulness
from skills.models import Skill


class PretestFormView(FormView):
    template_name = 'pretest_questionnaire.html'
    form_class = UserProfilePretestForm
    success_url = reverse_lazy('placement')


# Receives slug of subject, returns list of user skill levels for that subject in topological order
@api_view()
def get_subject_skills(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        skill_level_list = request.user.profile.get_subject_skills(kwargs.get("slug"))
        return Response({"skill_level_list": skill_level_list})


# Receives post request with kwarg pk and JSON with "new_skill_level" (decimal)
# Updates user's skill level of skill whose id=pk to new_skill_level
@api_view(['POST'])
@parser_classes([JSONParser])
def update_skill_level(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        data = request.data
        new_skill_level = float(data["new_skill_level"])
        user_profile.change_skill_level(kwargs.get("pk"), new_skill_level)
        return Response({"message": "success"})


# Receives post request with JSON with "confirmed_correct_skill_ids" (list of ints)
# Updates all confirmed skills and prerequisite skills with skill_level=0.9
@api_view(['POST'])
@parser_classes([JSONParser])
def post_placement_bulk_update(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        confirmed_correct_skill_ids = request.data["confirmed_correct_skill_ids"]
        all_known_skills = Skill.objects.get_prerequisite_skill_ids(confirmed_correct_skill_ids)
        Skillfulness.objects.filter(user_profile=user_profile).filter(pk__in=all_known_skills).update(skill_level=0.9)
        return Response({"message": "success"})
