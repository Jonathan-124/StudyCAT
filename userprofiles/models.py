from django.db import models
from django.contrib.auth import get_user_model
from skills.models import Skill, SkillEdge
from users.models import CustomUser
from curricula.models import Curriculum
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver


# UserProfile model - additional attributes to the user model not used for authentication
# user - one-to-one relationship to CustomUser model
# user_type - choice of what type of user they are
# skills - each UserProfile object has one relationship to every Skill object through the Skillfulness through model
# currently_studying - one-to-one relationship to Curriculum model, what the user is currently studying
# test_date - (if exists) what date the user will take their test
# user_type, currently_studying, test_date are fields updated in the pre-placement test questionnaire
class UserProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
    )

    CURRENT_STUDENT = 'CS'
    CAREER_RELATED = 'CR'
    MATHEMATICS_INSTRUCTOR = 'MI'
    SELF_STUDY = 'SS'

    USER_TYPES = [
        (CURRENT_STUDENT, 'Current Student'),
        (CAREER_RELATED, 'Career Related'),
        (MATHEMATICS_INSTRUCTOR, 'Mathematics Instructor'),
        (SELF_STUDY, 'Self Study'),
    ]
    user_type = models.CharField(max_length=2, choices=USER_TYPES, default=SELF_STUDY)
    skills = models.ManyToManyField(Skill, through='Skillfulness', through_fields=('user_profile', 'skill'))
    currently_studying = models.OneToOneField(Curriculum, on_delete=models.CASCADE, blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # Receives skill_id, return user's skill level of Skill object with id=skill_id
    def get_skill_level(self, num):
        skillobj = Skill.objects.get(id=num)
        skillfulness = self.user_skillfulness.get(skill=skillobj)
        return skillfulness.skill_level

    # Receives subject slug, returns list of user skill levels for subject skills in topological order
    def get_subject_skills(self, subject_slug):
        skill_level_list = self.user_skillfulness.filter(skill__subject__slug=subject_slug).order_by('skill__topological_order').values_list('skill_level', flat=True)
        return skill_level_list

    # Receives skill_id and n [0, 1], updates user skill proficiency of Skill object to new level
    # now defunct
    def change_skill_level(self, skill_id, n):
        newlevel = n
        skillfulness = self.user_skillfulness.get(skill__id=skill_id)
        if newlevel < 0:
            newlevel = 0
        elif newlevel > 1:
            newlevel = 1
        else:
            pass
        setattr(skillfulness, 'skill_level', newlevel)
        skillfulness.save()

    # Returns list of terminus skill ids
    def retrieve_terminus_skills(self):
        passed_skill_ids = Skillfulness.objects.filter(user_profile=self).filter(skill_level__gt=0.5).values_list('skill__id', flat=True)
        terminus_skill_ids = SkillEdge.objects.filter(parent_skill__id__in=passed_skill_ids).exclude(child_skill__id__in=passed_skill_ids).values_list('parent_skill__id', flat=True)
        return terminus_skill_ids

    # Receives num [1, 5], depreciates user skillfulness of the terminal-most skills
    # 1 - two days+; depreciate terminal skills slightly
    # 2 - one week+; depreciate terminal skills slightly more and and parents slightly
    # 3 - two weeks+; 4 - one month +; 5 - two months +;
    def depreciate_terminal_skills(self, num):
        terminus_skill_ids = self.retrieve_terminus_skills()
        while num > 0:
            depreciation = 0.6 - 0.1 * num
            Skillfulness.objects.filter(user_profile=self).filter(skill__id__in=terminus_skill_ids).update(skill_level=depreciation)
            terminus_skill_ids = self.retrieve_terminus_skills()
            num -= 1

    # Receives unit slug, returns percentage of skills in unit in which the user's skill_level > 0.5
    def unit_completion_percentage(self, unit_slug):
        unit_skillfulness = self.user_skillfulness.filter(skill__lesson__units__slug=unit_slug)
        percentage = unit_skillfulness.filter(skill_level__gt=0.5).count() / unit_skillfulness.count()
        return percentage

    # Receives curriculum id, list of objects with unit slug and their completion percentages
    def curriculum_units_completion_percentage(self, curriculum_id):
        percentages = []
        unit_slugs = Curriculum.objects.get(id=curriculum_id).units.values_list('slug', flat=True)
        for slug in unit_slugs:
            percentages.append({"slug": slug, "percentage": self.unit_completion_percentage(slug)})
        return percentages


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
    skill_level = models.DecimalField(decimal_places=3,
                                      max_digits=4,
                                      default=0)

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
