from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Questionnaire that updates fields in the user's profile
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_update.html'
