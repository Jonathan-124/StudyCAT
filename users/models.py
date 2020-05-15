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


user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')
user_logged_in.connect(update_previous_login, dispatch_uid='update_previous_login')
