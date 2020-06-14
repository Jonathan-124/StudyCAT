from django.db import models
from subjects.models import Subject
from units.models import Unit
from skills.models import Skill
from django.utils.text import slugify
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


# Curriculum model
# Each Curriculum object contains units related to a broad curriculum; each unit may belong to multiple curricula
# name - charfield of Curriculum name
# slug - name uniquely slugified, populated after save() is called
# start_skills - list of Skill object ids stored in JSON format; these are the root skills of the curriculum
# end_skills - list of Skill object ids stored in JSON format; these are the end-node skills of the curriculum
class Curriculum(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    start_skills = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    end_skills = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    subject = models.OneToOneField(Subject, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'curricula'

    def __str__(self):
        return self.name

    # Populates slug field with slugified curriculum name after save() is called
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Curriculum, self).save(*args, **kwargs)


# Called when Curriculum-Unit fk relationship added or removed
# Populates Curriculum object start_skills and end_skills fields by traversing the DAG
@receiver(post_save, sender=Unit, dispatch_uid='curriculum_unit_saved_signal')
def curriculum_unit_saved(sender, instance, **kwargs):
    # Acts when signal is in forward direction (instance is Curricula obj) and action that caused signal was add/remove
    curriculum = instance.curriculum
    start_skill_set = set()
    end_skill_set = set()
    skills = Skill.objects.filter(lesson__units__curriculum=curriculum)
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
    setattr(curriculum, 'start_skills', start_skill_list)
    setattr(curriculum, 'end_skills', end_skill_list)
    curriculum.save()

# Called when Unit-Lesson m2m relationship added or removed
# Populates Curriculum object start_skills and end_skills fields by traversing the DAG
@receiver(m2m_changed, sender=Unit.lessons.through)
def curriculum_lesson_relation_changed(sender, instance, action, reverse, **kwargs):
    # Acts when signal is in forward direction (instance is Unit obj) and action that caused signal was add/remove
    if not reverse and action == "post_add" or "post_remove":
        # Same code as above, but all curricula with units attribute that includes instance is updated
        curriculum = instance.curriculum
        start_skill_set = set()
        end_skill_set = set()
        skills = Skill.objects.filter(lesson__units__curriculum=curriculum)
        for i in skills:
            parents = i.get_parent_skills()
            children = i.get_children_skills()
            if not parents or parents.difference(skills):
                start_skill_set.add(i.id)
            if not children or children.difference(skills):
                end_skill_set.add(i.id)
        start_skill_list = list(start_skill_set)
        end_skill_list = list(end_skill_set.difference(start_skill_set))
        setattr(curriculum, 'start_skills', start_skill_list)
        setattr(curriculum, 'end_skills', end_skill_list)
        curriculum.save()
