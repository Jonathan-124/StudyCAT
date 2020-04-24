from django.urls import path
from .views import UnitView


urlpatterns = [
    path('<slug:slug>/', UnitView.as_view(), name='unit'),
]
