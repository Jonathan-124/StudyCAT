from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import UserProfile, CurrentlyStudying
from curricula.models import Curriculum


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type', )


class CurrentlyStudyingAddForm(ModelForm):
    class Meta:
        model = CurrentlyStudying
        exclude = ('user_profile', )

    def __init__(self, *args, **kwargs):
        super(CurrentlyStudyingAddForm, self).__init__(*args, **kwargs)
        self.fields['curriculum'].queryset = Curriculum.objects.exclude(id__in=kwargs['instance'].user_profile.currently_studying.all())
        self.fields['curriculum'].initial = False
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class CurrentlyStudyingUpdateForm(ModelForm):
    class Meta:
        model = CurrentlyStudying
        exclude = ('user_profile', )

    def __init__(self, *args, **kwargs):
        super(CurrentlyStudyingUpdateForm, self).__init__(*args, **kwargs)
        self.fields['curriculum'].disabled = True
        self.helper = FormHelper()
        self.helper.form_show_labels = False


CurrentlyStudyingAddFormSet = inlineformset_factory(UserProfile, CurrentlyStudying, form=CurrentlyStudyingAddForm, fields=('curriculum', 'test_date'), extra=0, can_delete=True)
CurrentlyStudyingUpdateFormSet = inlineformset_factory(UserProfile, CurrentlyStudying, form=CurrentlyStudyingUpdateForm, fields=('curriculum', 'test_date'), extra=0, can_delete=True)