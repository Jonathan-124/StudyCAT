from django.urls import path
from .views import LessonView, ExitTestView


urlpatterns = [
    path('<slug:slug>/', LessonView.as_view(), name='lesson'),
    path('<slug:slug>/test/', ExitTestView.as_view(), name='exit_test'),
]
