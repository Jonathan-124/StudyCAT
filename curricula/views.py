from django.views.generic import DetailView
from .models import Curriculum


class CurriculumView(DetailView):
    model = Curriculum
    template_name = "curriculum.html"
