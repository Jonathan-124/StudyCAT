from django.urls import path
from .views import PretestQuestionnaireView, update_skill_level, post_test_bulk_update


urlpatterns = [
    path('pretest-questionnaire/', PretestQuestionnaireView.as_view(), name='pretest-questionnaire'),
    path('posttest-update/', post_test_bulk_update, name='posttest_update'),
    path('posttest-update/<slug:slug>/', post_test_bulk_update, name='subject_posttest_update'),
    path('update/<int:pk>/', update_skill_level, name='update_skill_level'),
]
