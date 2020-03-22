from django.views.generic import DetailView
from .models import Unit
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class UnitView(DetailView):
    model = Unit
    template_name = "unit.html"


# Receives get request with unit id, returns list of dicts of user readiness for each lesson in the unit
# data is a list of {"lesson_slug": slug, "lesson_title": string, "readiness": int 0/1/2}, see userprofile method call
@api_view()
def ready_to_learn_lessons(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        data = user_profile.ready_to_learn_unit_lessons(kwargs.get('pk'))
        return Response({"lessons_readiness": data})
