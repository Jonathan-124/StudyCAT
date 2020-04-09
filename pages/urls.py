from django.urls import path
from .views import HomePageView, PlacementTestView, CreateGeneralBugReportView, CreateQuestionBugReportView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('general-report/', CreateGeneralBugReportView.as_view(), name='general-report'),
    path('question-report/', CreateQuestionBugReportView.as_view(), name='question-report'),
    path('placement/', PlacementTestView.as_view(), name='placement'),
]
