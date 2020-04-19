from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    previous_login = models.DateTimeField(null=True, blank=True)


def update_previous_login(sender, user, **kwargs):
    if not user.last_login:
        pass
    else:
        user.previous_login = user.last_login
        user.last_login = timezone.now()
        delta = (user.last_login - user.previous_login).days
        if delta < 2:
            pass
        elif delta < 7:
            user.profile.depreciate_terminal_skills(1)
        elif delta < 15:
            user.profile.depreciate_terminal_skills(2)
        elif delta < 30:
            user.profile.depreciate_terminal_skills(3)
        elif delta < 60:
            user.profile.depreciate_terminal_skills(4)
        else:
            user.profile.depreciate_terminal_skills(5)
        user.save(update_fields=['previous_login', 'last_login'])


user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')
user_logged_in.connect(update_previous_login, dispatch_uid='update_previous_login')
