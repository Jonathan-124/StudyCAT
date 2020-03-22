from django.urls import path
from .views import HomePageView, PlacementTestView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('placement/', PlacementTestView.as_view(), name='placement'),
]
