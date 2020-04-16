from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import Curriculum
from rest_framework.decorators import api_view
from rest_framework.response import Response


class CurriculumView(DetailView):
    model = Curriculum
    template_name = "curriculum.html"


@api_view()
@login_required()
def get_units_percentage_completion(request, *args, **kwargs):
    user_profile = request.user.profile
    data = user_profile.curriculum_units_completion_percentage(kwargs.get('pk'))
    return Response(data)
