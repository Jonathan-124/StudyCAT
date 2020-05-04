from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from subjects.models import Subject
from lessons.models import Lesson
from skills.models import Skill


# Unit model
# Each unit contains lessons related to a broad concept; each lesson may belong to multiple units
# name - charfield of name of unit
# slug - name uniquely slugified, populated after save() is called
# lessons - m2m field of lessons that are related to each unit
# start_skills - list of Skill object ids stored in JSON format; these are the root skills of the unit
# end_skills - list of Skill object ids stored in JSON format; these are the end-node skills of the unit
class Unit(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=255)
    lessons = models.ManyToManyField(Lesson, related_name='units')
    start_skills = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    end_skills = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    subject = models.OneToOneField(Subject, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    # Populates slug field with slugified unit name after save() is called
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Unit, self).save(*args, **kwargs)

    # Returns list of topological orders of all lessons in unit
    def lesson_topological_orders(self):
        lessons = self.lessons.select_related('skill')
        return list(map(lambda x: x.skill.topological_order, lessons))


# Called when Unit-Lesson m2m relationship added or removed
# Populates Unit object start_skills and end_skills fields by traversing the DAG
@receiver(m2m_changed, sender=Unit.lessons.through)
def lesson_unit_relation_changed(sender, instance, action, reverse, **kwargs):
    # Acts when signal is in forward direction (instance is Unit obj) and action that caused signal was add/remove
    if not reverse and action == "post_add" or "post_remove":
        # lessons - QuerySet of all lessons in Unit object that sent the signal
        # skills - list of all Skill objects associated with the lessons
        start_skill_set = set()
        end_skill_set = set()
        skills = Skill.objects.filter(lesson__units=instance)
        for i in skills:
            # Retrieve parents and children Skill objects for each i in skills object list
            # If i has no parents or if some parents are not in the skills object list, add i.id to start_skill_set
            # If i has no children or if some children are not in the skills object list, add i.id to end_skill_set
            parents = i.get_parent_skills()
            children = i.get_children_skills()
            if not parents or parents.difference(skills):
                start_skill_set.add(i.id)
            if not children or children.difference(skills):
                end_skill_set.add(i.id)
        # If a skill_id is in both the start and end skill sets, only include it in the start skill set
        # Add both lists into start_skill_dict and end_skill_dict, change to JSON, set model field attributes and save
        start_skill_list = list(start_skill_set)
        end_skill_list = list(end_skill_set.difference(start_skill_set))
        setattr(instance, 'start_skills', start_skill_list)
        setattr(instance, 'end_skills', end_skill_list)
        instance.save()
