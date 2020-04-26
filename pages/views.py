from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import CreateAPIView
from .models import GeneralBugReport, QuestionBugReport, LessonBugReport, UnitBugReport, CurriculumBugReport
from .serializers import GeneralBugReportSerializer, QuestionBugReportSerializer, LessonBugReportSerializer, UnitBugReportSerializer, CurriculumBugReportSerializer


class HomePageView(TemplateView):
    template_name = 'home.html'


class CreateGeneralBugReportView(LoginRequiredMixin, CreateAPIView):
    queryset = GeneralBugReport.objects.all()
    serializer_class = GeneralBugReportSerializer


class CreateQuestionBugReportView(LoginRequiredMixin, CreateAPIView):
    queryset = QuestionBugReport.objects.all()
    serializer_class = QuestionBugReportSerializer


class CreateLessonBugReportView(LoginRequiredMixin, CreateAPIView):
    queryset = LessonBugReport.objects.all()
    serializer_class = LessonBugReportSerializer


class CreateUnitBugReportView(LoginRequiredMixin, CreateAPIView):
    queryset = UnitBugReport.objects.all()
    serializer_class = UnitBugReportSerializer


class CreateCurriculumBugReportView(LoginRequiredMixin, CreateAPIView):
    queryset = CurriculumBugReport.objects.all()
    serializer_class = CurriculumBugReportSerializer

