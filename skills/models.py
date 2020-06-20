from django.contrib.postgres.fields import ArrayField
from django.db import models


# Additional methods for querying Skill objects
class SkillManager(models.Manager):
    # Receives list of skill ids, returns list of all prerequisite skill ids of input skills
    def get_prerequisite_skill_ids(self, id_list):
        id_set = set(id_list)
        prerequisite_skills_id_set = set()
        while id_set:
            current_id = id_set.pop()
            prerequisite_skills_id_set.add(current_id)
            preceding_skill_ids = self.get(id=current_id).get_preceding_skill_ids()
            id_set.update(set(preceding_skill_ids))
        return list(prerequisite_skills_id_set)


# Skill model - objects represent nodes of the DAG
# subject - fk to Subject, i.e. which subject area self belongs to
# name - name of skill
# related_skills - m2m field relating to other skills; asymmetric/hierarchical relationship, see SkillEdge
# topological order - numbered topological ordering of the skill DAG, see receiver/signal below
class Skill(models.Model):
    subject = models.ForeignKey('subjects.Subject', on_delete=models.PROTECT, related_name='skills')
    name = models.CharField(max_length=100)
    related_skills = models.ManyToManyField("self",
                                            through="SkillEdge",
                                            symmetrical=False,
                                            related_name="related_to")
    topological_order = models.PositiveIntegerField(blank=True, null=True)
    ancestor_ids = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    parents = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    children = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    descendant_ids = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    objects = SkillManager()

    class Meta:
        # Order skills by their topological order
        ordering = ['name']

    def __str__(self):
        return self.name

    # Returns QuerySet containing all children skills of self
    def get_children_skills(self):
        return self.related_skills.filter(children_skills__parent_skill=self)

    # Returns QuerySet containing all parent skills of self
    def get_parent_skills(self):
        return self.related_to.filter(parent_skills__child_skill=self)

    # Returns list of all prerequisite skill ids of self
    def get_preceding_skill_ids(self):
        ids = set()
        parent_skills = set(self.get_parent_skills())
        while parent_skills:
            current_skill = parent_skills.pop()
            ids.add(current_skill.id)
            parent_skills.update(set(current_skill.get_parent_skills()))
        return list(ids)

    def get_descendant_skill_ids(self):
        ids = set()
        child_skills = set(self.get_children_skills())
        while child_skills:
            current_skill = child_skills.pop()
            ids.add(current_skill.id)
            child_skills.update(set(current_skill.get_children_skills()))
        return list(ids)


# SkillEdge model - edges that connect Skill nodes in the knowledge DAG
class SkillEdge(models.Model):
    parent_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="parent_skills")
    child_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="children_skills")
    same_subject = models.BooleanField(default=True)

    def __str__(self):
        return self.parent_skill.name + " -> " + self.child_skill.name

    def save(self, *args, **kwargs):
        if self.parent_skill.subject == self.child_skill.subject:
            setattr(self, 'same_subject', True)
        else:
            setattr(self, 'same_subject', False)
        super(SkillEdge, self).save(*args, **kwargs)
