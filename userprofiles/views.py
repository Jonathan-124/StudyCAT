from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.generic.edit import UpdateView
from django.urls import reverse
from .models import UserProfile, Skillfulness
from django.core.exceptions import ValidationError


# Questionnaire that updates fields in the user's profile
class PretestQuestionnaireView(UpdateView):
    model = UserProfile
    fields = ('user_type', 'currently_studying', 'test_date')
    template_name = 'pretest_questionnaire.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self, queryset=None):
        return self.request.user.profile


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


# Receives post request with a JSON object {"update_via": str, "to_be_updated": list}
# if "updated_via" == "topological_order", list of {"topological_orders": [list of ints], "skill_level": float}
# if "updated_via" == "skill_ids", list of {"skill_ids": [list of ints], "skill_level": float}
# Updates all user skill_level for skillfulness objects with each of the given topological orders/skill ids
# Note: subject restricted for topological_order updates but not skill_id updates
@api_view(['POST'])
@parser_classes([JSONParser])
def post_test_bulk_update(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        if request.data["update_via"] == "topological_order":
            for obj in request.data["to_be_updated"]:
                Skillfulness.objects.filter(
                    user_profile=user_profile
                ).filter(
                    skill__subject__slug=kwargs.get("slug"), skill__topological_order__in=obj["topological_orders"]
                ).update(
                    skill_level=obj["skill_level"]
                )
            return Response({"message": "success"})
        elif request.data["update_via"] == "skill_ids":
            for obj in request.data["to_be_updated"]:
                Skillfulness.objects.filter(
                    user_profile=user_profile
                ).filter(
                    skill__id__in=obj["skill_ids"]
                ).update(
                    skill_level=obj["skill_level"]
                )
            return Response({"message": "success"})
        else:
            raise ValidationError
