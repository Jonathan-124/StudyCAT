from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import UserProfile, CurrentlyStudying


class CurrentlyStudyingUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type', 'currently_studying')


CurrentlyStudyingFormSet = inlineformset_factory(UserProfile, CurrentlyStudying, fields=('curriculum', 'test_date'))
