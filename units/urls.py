from django.urls import path
from .views import UnitView, get_unit_data, get_unit_percentage_completion


urlpatterns = [
    path('<slug:slug>/', UnitView.as_view(), name='unit'),
    path('data/<int:pk>/', get_unit_data, name='get_unit_data'),
    path('readiness/<slug:slug>/', get_unit_percentage_completion, name='get_unit_percentage_completion'),
]
