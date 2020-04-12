from django.urls import path
from .views import get_subject_data, PlacementTestView


urlpatterns = [
    path('<slug:slug>/', get_subject_data, name='get_subject_data'),
    path('placement/<slug:slug>/', PlacementTestView.as_view(), name='placement'),
]
