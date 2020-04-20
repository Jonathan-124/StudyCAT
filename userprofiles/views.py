from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.views.generic.edit import UpdateView
from django.urls import reverse
from .models import UserProfile, Skillfulness
from .forms import CurrentlyStudyingUpdateForm, CurrentlyStudyingFormSet
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Questionnaire that updates fields in the user's profile
class PretestQuestionnaireView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = CurrentlyStudyingUpdateForm
    template_name = 'pretest_questionnaire.html'

    def get_success_url(self):
        return reverse('home')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        currently_studying_form = CurrentlyStudyingFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, currently_studying_form=currently_studying_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        currently_studying_form = CurrentlyStudyingFormSet()
        if form.is_valid() and currently_studying_form.is_valid():
            return self.form_valid(form, currently_studying_form)
        else:
            return self.form_invalid(form, currently_studying_form)

    def form_valid(self, form, currently_studying_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        currently_studying_form.instance = self.object
        currently_studying_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, currently_studying_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, currently_studying_form=currently_studying_form))


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
