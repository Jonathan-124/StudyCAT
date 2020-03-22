from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'


class PlacementTestView(TemplateView):
    template_name = 'placement_test.html'
