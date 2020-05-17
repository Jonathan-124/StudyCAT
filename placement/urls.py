from django.urls import path
from .views import PlacementTestView

urlpatterns = [
    path('<int:pk>/', PlacementTestView.as_view(), name='initial_placement_test'),
]
