from django.forms import ModelForm
from .models import UserProfile


class UserProfilePretestForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('user_type', 'currently_studying', 'test_date')
