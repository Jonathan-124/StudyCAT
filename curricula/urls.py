from django.urls import path
from .views import CurriculumView, get_units_percentage_completion

urlpatterns = [
    path('<slug:slug>/', CurriculumView.as_view(), name='curriculum'),
    path('readiness/<int:pk>/', get_units_percentage_completion, name='get_units_percentage_completion'),
]
