from django.urls import path
from .views import get_homepage_data, get_curriculum_completion_status, get_unit_data, get_parent_lessons_data, get_random_questions, get_related_questions, post_test_update, post_placement_bulk_update, get_placement_question_pack

urlpatterns = [
    path('homepage-data/', get_homepage_data, name='get_homepage_data'),
    path('curriculum/status/<int:pk>/', get_curriculum_completion_status, name='get_curriculum_completion_status'),
    path('units/<int:pk>/', get_unit_data, name='get_unit_data'),
    path('lessons/<int:pk>/', get_parent_lessons_data, name='get_parent_lessons_data'),
    path('questions/random/<int:pk>/', get_random_questions, name='get_random_question'),
    path('questions/random/<int:pk>/<int:num>/', get_random_questions, name='get_random_questions'),
    path('questions/<slug:relation>/<int:pk>/', get_related_questions, name='get_related_questions'),
    path('update/', post_test_update, name='post_test_update'),
    path('bulk-update/', post_placement_bulk_update, name='post_placement_bulk_update'),
    path('<slug:scope>/placement-pack/', get_placement_question_pack, name='get_refresher_question_pack'),
    path('<slug:scope>/placement-pack/<int:pk>', get_placement_question_pack, name='get_placement_question_pack'),
]
