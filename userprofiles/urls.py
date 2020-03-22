from django.urls import path
from .views import PretestFormView, get_skill_level, update_skill_level, post_placement_bulk_update, get_skill_readiness_status

urlpatterns = [
    path('pretest-questionnaire/', PretestFormView.as_view()),
    path('posttest-update/', post_placement_bulk_update),
    path('skill-level/<int:pk>/', get_skill_level),
    path('update/<int:pk>/', update_skill_level),
    path('readiness/<int:pk>/', get_skill_readiness_status)
]
