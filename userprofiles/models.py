from django.db import models
from django.contrib.auth import get_user_model
from skills.models import Skill
from users.models import CustomUser
from units.models import Unit
'''from curricula.models import Curriculum'''
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver


# Additional manager methods for Skillfulness model QuerySets
class SkillfulnessManager(models.Manager):
    # Receives userprofile object and list of skill_ids, returns user readiness to learn each skill in list
    def unit_readiness(self, userprofile, skill_id_list):
        self.filter(user_profile=userprofile)


'''To add back currently_studying field after Curriculum app created and to create form'''
# UserProfile are additional attributes to the user model not used for authentication
class UserProfile(models.Model):
    # user - one-to-one relationship to CustomUser model
    # user_type - choice of what type of user they are
    # skills - each UserProfile object has one relationship to every Skill object through the Skillfulness through model
    # currently_studying - one-to-one relationship to Curriculum model, what the user is currently studying
    # test_date - (if exists) what date the user will take their test
    # user_type, currently_studying, test_date are fields updated in the pre-placement test questionnaire
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
    '''currently_studying = models.OneToOneField(Curriculum, on_delete=models.CASCADE, blank=True, null=True)'''
    test_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # Receives skill_id, return user's skill level of Skill object with id=skill_id
    def get_skill_level(self, num):
        skillobj = Skill.objects.get(id=num)
        skillfulness = self.user_skillfulness.get(skill=skillobj)
        return skillfulness.skill_level

    # Receives skill_id and n [0, 1], updates user skill proficiency of Skill object to new level
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

    # Receives skill_id, returns int that indicates whether user is ready to learn skill
    # Return 2 (already learned) if user's skill_level for >= 0.5
    # Return 1 (ready to learn) if all skill_level of parent skills >= 0.5
    # Return 0 (not ready to learn) if some skill_level of parent skills < 0.5
    # to un-hardcode threshold!
    def ready_to_learn_skill(self, skill_id):
        skillobj = Skill.objects.get(id=skill_id)
        skillfulness = self.user_skillfulness.get(skill=skillobj)
        if Decimal(skillfulness.skill_level) >= 0.5:
            return 2
        else:
            parent_skills = skillobj.get_parent_skills()
            incomplete = list(
                filter(lambda x: (x.user_skillfulness.get(user_profile=self.user_profile).skill_level < 0.5),
                       parent_skills)
            )
            if incomplete:
                return 0
            else:
                return 1

    # Receives unit id, returns list of dicts of lesson slug, name, and user readiness for all lessons in unit
    def ready_to_learn_unit_lessons(self, unit_id):
        data = []
        skills = Unit.objects.get(id=unit_id).lessons.select_related('skill').all()
        for skill in skills:
            skillfulness = self.user_skillfulness.get(skill=skill)
            readiness = 0
            if Decimal(skillfulness.skill_level) >= 0.5:
                readiness = 2
            else:
                parent_skills = skill.get_parent_skills()
                incomplete = list(
                    filter(lambda x: (x.user_skillfulness.get(user_profile=self.user_profile).skill_level < 0.5),
                           parent_skills)
                )
                if incomplete:
                    pass
                else:
                    readiness = 1
            data.append({"lesson_slug": skill.lesson.slug, "lesson_title": skill.lesson.name, "readiness": readiness})
        return data

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
class Skillfulness(models.Model):
    # user_profile - one-to-one relation to UserProfile object
    # skill - one-to-one relation to Skill object
    # skill_level - [0, 1] of user's skill level for a Skill object
    # to add standard deviation - 'confidence' field?
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_skillfulness')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skillfulness')
    skill_level = models.DecimalField(decimal_places=3,
                                      max_digits=4,
                                      default=0)

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
