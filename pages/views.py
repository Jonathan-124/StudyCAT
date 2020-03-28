from django.views.generic import TemplateView
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView
from .models import GeneralBugReport, QuestionBugReport
from .serializers import GeneralBugReportSerializer, QuestionBugReportSerializer


class HomePageView(TemplateView):
    template_name = 'home.html'


class PlacementTestView(TemplateView):
    template_name = 'placement_test.html'


class CreateGeneralBugReportView(CreateAPIView):
    queryset = GeneralBugReport.objects.all()
    serializer_class = GeneralBugReportSerializer


class CreateQuestionBugReportView(CreateAPIView):
    queryset = QuestionBugReport.objects.all()
    serializer_class = QuestionBugReportSerializer


def login_redirect_view(request):
    if request.user.is_anonymous:
        return redirect('home')
    else:
        try:
            curriculum = request.user.profile.currently_studying
            return redirect(curriculum)
        except:
            return redirect('pretest-questionnaire')
