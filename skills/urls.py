from django.urls import path
from .views import skill_based_randomizer, skill_question_pack, parent_skill_question_pack, children_skill_question_pack

urlpatterns = [
    path('random/<int:pk>/', skill_based_randomizer),
    path('random-pack/<int:pk>/', skill_question_pack),
    path('random-pack/<int:pk>/<int:num>/', skill_question_pack),
    path('parents-pack/<int:pk>/', parent_skill_question_pack),
    path('children-pack/<int:pk>/', children_skill_question_pack),
]
