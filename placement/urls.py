from django.urls import path
from .views import PlacementTestView, initial_question_pack

urlpatterns = [
    path('<slug:scope>/<int:pk>/', PlacementTestView.as_view(), name='initial_placement_test'),
    path('initial-questions/', initial_question_pack, name='initial_question_pack'),
]
