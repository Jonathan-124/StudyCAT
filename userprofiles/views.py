from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.generic.edit import UpdateView
from django.urls import reverse
from .models import UserProfile, Skillfulness
from .forms import ProfileUpdateForm, CurrentlyStudyingFormSet
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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
            context['currently_studying_form'] = CurrentlyStudyingFormSet(self.request.POST, instance=self.get_object())
        else:
            context['currently_studying_form'] = CurrentlyStudyingFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        currently_studying_form = context['currently_studying_form']
        with transaction.atomic():
            self.object = form.save()
            if currently_studying_form.is_valid():
                currently_studying_form.instance = self.get_object()
                currently_studying_form.save()
        return super(ProfileUpdateView, self).form_valid(form)


# Receives post request with kwarg pk and JSON with "new_skill_level" (decimal)
# Updates user's skill level of skill whose id=pk to new_skill_level
@api_view(['POST'])
@login_required()
@parser_classes([JSONParser])
def update_skill_level(request, *args, **kwargs):
    user_profile = request.user.profile
    data = request.data
    new_skill_level = float(data["new_skill_level"])
    user_profile.change_skill_level(kwargs.get("pk"), new_skill_level)
    return Response({"message": "success"})


# Receives post request with a JSON object {"update_via": str, "to_be_updated": list}
# if "updated_via" == "topological_order", list of {"topological_orders": [list of ints], "skill_level": float}
# if "updated_via" == "skill_ids", list of {"skill_ids": [list of ints], "skill_level": float}
# Updates all user skill_level for skillfulness objects with each of the given topological orders/skill ids
# Note: subject restricted for topological_order updates but not skill_id updates
@api_view(['POST'])
@login_required()
@parser_classes([JSONParser])
def post_test_bulk_update(request, *args, **kwargs):
    user_profile = request.user.profile
    if request.data["update_via"] == "topological_order":
        for obj in request.data["to_be_updated"]:
            Skillfulness.objects.filter(
                user_profile=user_profile
            ).filter(
                skill__subject__slug=kwargs.get("slug"), skill__topological_order__in=obj["topological_orders"]
            ).update(
                skill_level=obj["skill_level"]
            )
        return Response({"message": "success"})
    elif request.data["update_via"] == "skill_ids":
        for obj in request.data["to_be_updated"]:
            Skillfulness.objects.filter(
                user_profile=user_profile
            ).filter(
                skill__id__in=obj["skill_ids"]
            ).update(
                skill_level=obj["skill_level"]
            )
        return Response({"message": "success"})
    else:
        raise ValidationError
