from django.views.generic import DetailView
from .models import Curriculum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class CurriculumView(DetailView):
    model = Curriculum
    template_name = "curriculum.html"


@api_view()
def get_units_percentage_completion(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        data = user_profile.curriculum_units_completion_percentage(kwargs.get('pk'))
        return Response(data)
