from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import UserProfile, CurrentlyStudying


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type', )


class CurrentlyStudyingForm(ModelForm):
    class Meta:
        model = CurrentlyStudying
        exclude = ('user_profile', )

    def __init__(self, *args, **kwargs):
        super(CurrentlyStudyingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


CurrentlyStudyingFormSet = inlineformset_factory(UserProfile, CurrentlyStudying, form=CurrentlyStudyingForm, fields=('curriculum', 'test_date'), extra=0, can_delete=True)
