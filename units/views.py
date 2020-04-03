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
