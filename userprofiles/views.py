from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .forms import UserProfilePretestForm
from django.views.generic.edit import FormView
from .models import Skillfulness
from skills.models import Skill


class PretestFormView(FormView):
    template_name = 'pretest_questionnaire.html'
    form_class = UserProfilePretestForm
    success_url = '/home/'


# Receives get request with kwarg pk and returns JSON response of user's skill_level of skill with id=pk
@api_view()
def get_skill_level(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        level = user_profile.get_skill_level(kwargs.get("pk"))
        return Response({"lvl": level})


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


# Receives get request with kwarg pk, returns user readiness of learning skill with id=pk
@api_view()
def get_skill_readiness_status(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        readiness = user_profile.ready_to_learn_skill(kwargs.get("pk"))
    return Response({"readiness": readiness})
