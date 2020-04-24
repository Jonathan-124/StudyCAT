from django.urls import path
from .views import CurriculumView

urlpatterns = [
    path('<slug:slug>/', CurriculumView.as_view(), name='curriculum'),
]
