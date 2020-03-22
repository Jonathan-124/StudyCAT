from django.urls import path
from .views import UnitView, ready_to_learn_lessons


urlpatterns = [
    path('<slug:slug>/', UnitView.as_view(), name='unit'),
    path('readiness/<int:pk>/', ready_to_learn_lessons)
]
