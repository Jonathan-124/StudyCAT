import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from questions.models import Question


class CustomUser(AbstractUser):
    previous_login = models.DateTimeField(null=True, blank=True)


def update_previous_login(sender, user, **kwargs):
    if not user.last_login:
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
    else:
        user.previous_login = user.last_login
        user.last_login = timezone.now()
        user.save(update_fields=['previous_login', 'last_login'])
        userprofile = user.profile
        terminus_skill_ids = userprofile.retrieve_terminus_skills()
        if not userprofile.last_lesson_completion:
            userprofile.streak_start = timezone.now()
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
                userprofile.depreciate_terminal_skills(1, terminus_skill_ids)
            elif delta < 15:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(2, terminus_skill_ids)
            elif delta < 30:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(3, terminus_skill_ids)
            elif delta < 60:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(4, terminus_skill_ids)
            else:
                userprofile.streak_start = timezone.now()
                userprofile.depreciate_terminal_skills(5, terminus_skill_ids)
        if (user.last_login - user.previous_login).days > 0 and terminus_skill_ids:
            qotd = Question.objects.random(random.choice(terminus_skill_ids)).id
            userprofile.qotd = qotd
        userprofile.save(update_fields=['streak_start', 'last_lesson_completion', 'qotd'])


user_logged_in.disconnect(update_last_login, dispatch_uid='update_last_login')
user_logged_in.connect(update_previous_login, dispatch_uid='update_previous_login')
