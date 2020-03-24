from .models import Subject
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def get_subject_dependency_matrix(request, *args, **kwargs):
    matrix = Subject.objects.get(slug=kwargs.get('slug')).dependencies
    return Response({"dependency_matrix": matrix})
