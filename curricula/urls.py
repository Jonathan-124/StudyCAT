from django.urls import path
from .views import CurriculumView, ready_to_learn_units, get_placement_initial_question_pack

urlpatterns = [
    path('<slug:slug>/', CurriculumView.as_view(), name='curriculum'),
    path('readiness/<int:pk>/', ready_to_learn_units),
    path('placement-test/initial-questions/', get_placement_initial_question_pack),
]
