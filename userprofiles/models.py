import random
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from skills.models import Skill, SkillEdge
from users.models import CustomUser
from curricula.models import Curriculum


# UserProfile model - additional attributes to the user model not used for authentication
# user - one-to-one relationship to CustomUser model
# skills - each UserProfile object has one relationship to every Skill object through the Skillfulness through model
# currently_studying - one-to-one relationship to Curriculum model, what the user is currently studying
# test_date - (if exists) what date the user will take their test
class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
    )
    currently_studying = models.ManyToManyField(Curriculum, through='CurrentlyStudying', through_fields=('user_profile', 'curriculum'))
    skills = models.ManyToManyField(Skill, through='Skillfulness', through_fields=('user_profile', 'skill'))
    streak_start = models.DateTimeField(null=True, blank=True)
    last_lesson_completion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    # Receives skill_id, return user's skill level of Skill object with id=skill_id
    def get_skill_level(self, num):
        skillobj = Skill.objects.get(id=num)
        skillfulness = self.user_skillfulness.get(skill=skillobj)
        return skillfulness.skill_level

    # Returns list of terminus skill ids
    def retrieve_terminus_skills(self):
        terminus_skill_ids = []
        passed_skills = Skill.objects.filter(user_skillfulness__user_profile=self).filter(user_skillfulness__skill_level__gte=1)
        terminus_skilledges = SkillEdge.objects.filter(parent_skill__in=passed_skills).exclude(child_skill__in=passed_skills).select_related('parent_skill')
        for skilledge in terminus_skilledges:
            if not skilledge.parent_skill.get_children_skills().intersection(passed_skills):
                terminus_skill_ids.append(skilledge.parent_skill.id)
        return terminus_skill_ids

    # Returns queryset of terminus lessons and random skill id of one of these lessons
    def retrieve_terminus_lessons(self):
        lessons = set()
        passed_skills = Skillfulness.objects.filter(user_profile=self).filter(skill_level__gte=1)
        terminus_skills = SkillEdge.objects.filter(parent_skill__id__in=passed_skills).exclude(child_skill__id__in=passed_skills).select_related('parent_skill__lesson')
        if not passed_skills:
            terminus_skills = Skill.objects.filter(parents__len=0)
            for skill in terminus_skills:
                lessons.add(skill.lesson)
            return lessons, random.choice(terminus_skills).id
        elif not terminus_skills:
            terminus_skills = Skill.objects.filter(children__len=0)
            for skill in terminus_skills:
                lessons.add(skill.lesson)
            return lessons, random.choice(terminus_skills).id
        else:
            for skilledge in terminus_skills:
                lessons.add(skilledge.parent_skill.lesson)
            return lessons, random.choice(terminus_skills).parent_skill.id

    # Receives num [1, 5], depreciates user skillfulness of the terminal-most skills
    # 1 - two days+; depreciate terminal skills slightly
    # 2 - one week+; depreciate terminal skills slightly more and and parents slightly
    # 3 - two weeks+; 4 - one month +; 5 - two months +;
    def depreciate_terminal_skills(self, num):
        terminus_skills = self.retrieve_terminus_skills()
        while num > 0:
            Skillfulness.objects.filter(user_profile=self).filter(skill__id__in=terminus_skills).update(skill_level=models.F('skill_level') - 1)
            terminus_skills = self.retrieve_terminus_skills()
            num -= 1

    # Receives unit slug, returns tuple of counts
    def unit_completion_percentage(self, unit_slug):
        unit_skillfulness = self.user_skillfulness.filter(skill__lesson__units__slug=unit_slug)
        return unit_skillfulness.filter(skill_level__gte=1).count(), unit_skillfulness.count()

    # Receives curriculum, list of objects with unit slug and their completion tuples
    def curriculum_units_completion_percentage(self, curriculum_obj):
        status = []
        unit_slugs = curriculum_obj.units.values_list('slug', flat=True)
        for slug in unit_slugs:
            status.append({"slug": slug, "status": self.unit_completion_percentage(slug)})
        return status


# Creates UserProfile object when CustomUser is created
@receiver(post_save, sender=CustomUser, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

# Saves UserProfile object when CustomUser is saved
@receiver(post_save, sender=CustomUser, dispatch_uid='save_user_profile')
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Custom through model that connects one UserProfile object to one Skill object
# user_profile - one-to-one relation to UserProfile object
# skill - one-to-one relation to Skill object
# skill_level - [0, 1] of user's skill level for a Skill object
# to add standard deviation - 'confidence' field?
class Skillfulness(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_skillfulness')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skillfulness')
    skill_level = models.SmallIntegerField(default=0)

    class Meta:
        order_with_respect_to = 'skill'

    def __str__(self):
        return self.skill.name


# Creates Skillfulness object for each user that connects UserProfile to skill when a new Skill object is created
@receiver(post_save, sender=Skill, dispatch_uid='create_user_skill')
def create_user_skill(sender, instance, created, **kwargs):
    if created:
        all_user_profiles = UserProfile.objects.all()
        for oneuser in all_user_profiles:
            Skillfulness.objects.get_or_create(user_profile=oneuser, skill=instance)

# Creates all Skillfulness objects for a new UserProfile that connects to all existing Skill objects
@receiver(post_save, sender=UserProfile, dispatch_uid='create_all_skills')
def create_all_skills(sender, instance, created, **kwargs):
    if created:
        all_skills = Skill.objects.all()
        for i in all_skills:
            Skillfulness.objects.get_or_create(user_profile=instance, skill=i)


class CurrentlyStudying(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='currently_studying_through')
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='currently_studying_through')
    test_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding and CurrentlyStudying.objects.filter(user_profile=self.user_profile, curriculum=self.curriculum).exists():
            raise ValidationError('Cannot create a currently studying object as user already has one.')
        return super(CurrentlyStudying, self).save(*args, **kwargs)
