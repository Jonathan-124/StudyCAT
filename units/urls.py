from django.urls import path
from .views import UnitView, ready_to_learn_lessons, get_unit_data


urlpatterns = [
    path('<slug:slug>/', UnitView.as_view(), name='unit'),
    path('data/<int:pk>/', get_unit_data, name='get_unit_data'),
    path('readiness/<int:pk>/', ready_to_learn_lessons, name='unit_readiness')
]
