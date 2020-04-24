from django.urls import path
from .views import PlacementTestView

urlpatterns = [
    path('<slug:scope>/<int:pk>/', PlacementTestView.as_view(), name='initial_placement_test'),
]
