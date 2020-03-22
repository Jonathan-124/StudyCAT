from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lesson


# Lesson class based view that extends 'lesson.html' template with lesson_text
class LessonView(DetailView):
    model = Lesson
    template_name = 'lesson.html'


# Class based view for exit test after user finishes a lesson; requires user to be logged in
class ExitTestView(LoginRequiredMixin, DetailView):
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(ExitTestView, self).dispatch(request, *args, **kwargs)
    model = Lesson
    template_name = 'exit_test.html'
    login_url = '/users/login/'
