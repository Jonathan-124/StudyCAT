from .models import Subject
from .serializers import SubjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def get_subject_data(request, *args, **kwargs):
    subject_data = SubjectSerializer(Subject.objects.get(slug=kwargs.get('slug'))).data
    if request.user.is_anonymous:
        return Response({"subject_data": subject_data})
    else:
        skill_level_list = request.user.profile.get_subject_skills(kwargs.get("slug"))
        return Response({"subject_data": subject_data, "skill_level_list": skill_level_list})
