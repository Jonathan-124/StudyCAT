from django.urls import path
from .views import UnitView, UnitReviewView


urlpatterns = [
    path('<slug:slug>/', UnitView.as_view(), name='unit'),
    path('<slug:slug>/review/', UnitReviewView.as_view(), name='unit_review'),
]
