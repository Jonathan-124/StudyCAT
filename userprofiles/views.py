from django.views.generic.edit import UpdateView
from django.urls import reverse
from .models import UserProfile
from .forms import ProfileUpdateForm, CurrentlyStudyingAddFormSet, CurrentlyStudyingUpdateFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction


# Questionnaire that updates fields in the user's profile
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm
    template_name = 'profile_update.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['currently_studying_add_form'] = CurrentlyStudyingAddFormSet(self.request.POST, instance=self.get_object())
            context['currently_studying_update_form'] = CurrentlyStudyingUpdateFormSet(self.request.POST, instance=self.get_object())
        else:
            context['currently_studying_add_form'] = CurrentlyStudyingAddFormSet(instance=self.get_object())
            context['currently_studying_update_form'] = CurrentlyStudyingUpdateFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        currently_studying_add_form = context['currently_studying_form']
        currently_studying_update_form = context['currently_studying_form']
        with transaction.atomic():
            self.object = form.save()
            if currently_studying_add_form.is_valid() and currently_studying_update_form.is_valid():
                currently_studying_add_form.instance = self.get_object()
                currently_studying_add_form.save()
                currently_studying_update_form.instance = self.get_object()
                currently_studying_update_form.save()
        return super(ProfileUpdateView, self).form_valid(form)
