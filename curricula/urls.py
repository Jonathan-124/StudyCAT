from django.urls import path
from .views import CurriculumView, get_units_percentage_completion, get_placement_initial_question_pack

urlpatterns = [
    path('<slug:slug>/', CurriculumView.as_view(), name='curriculum'),
    path('readiness/<int:pk>/', get_units_percentage_completion, name='get_units_percentage_completion'),
    path('placement-test/initial-questions/', get_placement_initial_question_pack, name='placement_initial_questions'),
]
