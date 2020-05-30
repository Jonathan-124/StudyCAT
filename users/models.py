from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in


class CustomUser(AbstractUser):
    previous_login = models.DateTimeField(null=True, blank=True)


def update_previous_login(sender, user, **kwargs):
    if not user.last_login:
        pass
    else:
        user.previous_login = user.last_login
        user.last_login = timezone.now()
        user.save(update_fields=['previous_login', 'last_login'])
        userprofile = user.profile
        if not userprofile.last_lesson_completion:
            userprofile.streak_start = timezone.now()
            userprofile.last_lesson_completion = timezone.now()
            userprofile.save(update_fields=['streak_start', 'last_lesson_completion'])
        elif userprofile.last_lesson_completion == timezone.now():
            pass
        else:
            delta = (userprofile.last_lesson_completion - userprofile.streak_start).days
            if delta == 1:
                pass
            elif delta < 3:
                userprofile.streak_start = timezone.now()
            elif delta < 7:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(1)
            elif delta < 15:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(2)
            elif delta < 30:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(3)
            elif delta < 60:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(4)
            else:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(5)
            userprofile.save(update_fields=['streak_start', 'last_lesson_completion'])


user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')
user_logged_in.connect(update_previous_login, dispatch_uid='update_previous_login')
