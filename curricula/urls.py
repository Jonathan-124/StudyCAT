from django.urls import path
from .views import CurriculumView, get_placement_initial_question_pack

urlpatterns = [
    path('<slug:slug>/', CurriculumView.as_view(), name='curriculum'),
    path('placement-test/initial-questions/', get_placement_initial_question_pack),
]
