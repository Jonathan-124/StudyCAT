from django.views.generic import DetailView
from .models import Lesson


# Lesson class based view that extends 'lesson.html' template with lesson_text
class LessonView(DetailView):
    model = Lesson
    template_name = 'lesson.html'


# Class based view for exit test after user finishes a lesson; requires user to be logged in
class ExitTestView(DetailView):
    model = Lesson
    template_name = 'exit_test.html'
