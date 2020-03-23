from django.views.generic import TemplateView
from django.shortcuts import redirect


class HomePageView(TemplateView):
    template_name = 'home.html'


class PlacementTestView(TemplateView):
    template_name = 'placement_test.html'


def login_redirect_view(request):
    if request.user.is_anonymous:
        return redirect('home')
    else:
        try:
            curriculum = request.user.profile.currently_studying
            return redirect(curriculum)
        except:
            return redirect('pretest-questionnaire')
