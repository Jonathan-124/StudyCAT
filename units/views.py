from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Unit


class UnitView(DetailView):
    model = Unit
    template_name = "unit.html"


class UnitReviewView(LoginRequiredMixin, DetailView):
    model = Unit
    template_name = "unit_review.html"
