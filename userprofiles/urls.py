from django.urls import path
from .views import PretestFormView, get_subject_skills, update_skill_level, post_placement_bulk_update


urlpatterns = [
    path('pretest-questionnaire/', PretestFormView.as_view(), name='pretest-questionnaire'),
    path('posttest-update/', post_placement_bulk_update, name='posttest_update'),
    path('subject-skills/<slug:slug>/', get_subject_skills, name='get_subject_skills'),
    path('update/<int:pk>/', update_skill_level, name='update_skill_level'),
]
