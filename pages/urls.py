from django.urls import path
from .views import HomePageView, CreateGeneralBugReportView, CreateQuestionBugReportView, CreateLessonBugReportView, \
    CreateUnitBugReportView, CreateCurriculumBugReportView, AboutPageView, FAQPageView, RoadmapPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('general-report/', CreateGeneralBugReportView.as_view(), name='general-report'),
    path('question-report/', CreateQuestionBugReportView.as_view(), name='question-report'),
    path('lesson-report/', CreateLessonBugReportView.as_view(), name='lesson-report'),
    path('unit-report/', CreateUnitBugReportView.as_view(), name='unit-report'),
    path('curriculum-report/', CreateCurriculumBugReportView.as_view(), name='curriculum-report'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('faq/', FAQPageView.as_view(), name='faq'),
    path('roadmap/', RoadmapPageView.as_view(), name='roadmap'),
]
