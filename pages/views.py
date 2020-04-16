from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import CreateAPIView
from .models import GeneralBugReport, QuestionBugReport
from .serializers import GeneralBugReportSerializer, QuestionBugReportSerializer


class HomePageView(TemplateView):
    template_name = 'home.html'


class CreateGeneralBugReportView(LoginRequiredMixin, CreateAPIView):
    queryset = GeneralBugReport.objects.all()
    serializer_class = GeneralBugReportSerializer


class CreateQuestionBugReportView(LoginRequiredMixin, CreateAPIView):
    queryset = QuestionBugReport.objects.all()
    serializer_class = QuestionBugReportSerializer
