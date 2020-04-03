from django.views.generic import DetailView
from .models import Unit
from .serializers import UnitSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class UnitView(DetailView):
    model = Unit
    template_name = "unit.html"


@api_view()
def get_unit_data(request, *args, **kwargs):
    unit = Unit.objects.get(id=kwargs.get('pk'))
    unit_data = UnitSerializer(unit).data
    return Response(unit_data)


@api_view()
def get_unit_percentage_completion(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        user_profile = request.user.profile
        percentage = user_profile.unit_completion_percentage(kwargs.get('slug'))
        return Response({"percentage": percentage})
