from django.urls import path
from .views import skill_based_randomizer, skill_question_pack, parent_skill_question_pack, children_skill_question_pack, get_lesson_data_from_topological_order

urlpatterns = [
    path('homepage-data/', get_lesson_data_from_topological_order, name='homepage-data'),
    path('random/', skill_based_randomizer, name='skill_based_randomizer'),
    path('random-pack/<int:pk>/', skill_question_pack, name='skill_question_pack'),
    path('random-pack/<int:pk>/<int:num>/', skill_question_pack),
    path('parents-pack/<int:pk>/', parent_skill_question_pack, name='parent_skill_question_pack'),
    path('children-pack/<int:pk>/', children_skill_question_pack, name='children_skill_question_pack'),
]
