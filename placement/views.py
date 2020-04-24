from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PlacementTestView(LoginRequiredMixin, TemplateView):
    template_name = 'placement_test.html'
