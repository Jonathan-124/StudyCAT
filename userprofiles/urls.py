from django.urls import path
from .views import ProfileUpdateView, update_skill_level, post_test_bulk_update


urlpatterns = [
    path('profile-update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('posttest-update/', post_test_bulk_update, name='posttest_update'),
    path('posttest-update/<slug:slug>/', post_test_bulk_update, name='subject_posttest_update'),
    path('update/<int:pk>/', update_skill_level, name='update_skill_level'),
]
