from django.urls import path
from .views import get_subject_data


urlpatterns = [
    path('<slug:slug>/', get_subject_data, name='get_subject_data'),
]
