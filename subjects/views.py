from .models import Subject
from .serializers import SubjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def get_subject_dependency_matrix(request, *args, **kwargs):
    subject_data = SubjectSerializer(Subject.objects.get(slug=kwargs.get('slug'))).data
    return Response(subject_data)
