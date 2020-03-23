from django.urls import path
from .views import HomePageView, PlacementTestView, login_redirect_view


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login-redirect', login_redirect_view, name='login_redirect'),
    path('placement/', PlacementTestView.as_view(), name='placement'),
]
