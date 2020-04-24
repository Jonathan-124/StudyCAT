from django.views.generic import DetailView
from .models import Unit


class UnitView(DetailView):
    model = Unit
    template_name = "unit.html"
