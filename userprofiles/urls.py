from django.urls import path
from .views import PretestQuestionnaireView, update_skill_level, post_placement_bulk_update


urlpatterns = [
    path('pretest-questionnaire/', PretestQuestionnaireView.as_view(), name='pretest-questionnaire'),
    path('posttest-update/', post_placement_bulk_update, name='posttest_update'),
    path('update/<int:pk>/', update_skill_level, name='update_skill_level'),
]
