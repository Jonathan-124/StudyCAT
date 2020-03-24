from django.urls import path
from .views import get_subject_dependency_matrix


url_patterns = [
    path('<slug:slug>/', get_subject_dependency_matrix, name='get_subject_dependency_matrix'),
]
