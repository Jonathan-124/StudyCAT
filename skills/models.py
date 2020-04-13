from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from subjects.models import Subject


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
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='skills')
    name = models.CharField(max_length=100)
    related_skills = models.ManyToManyField("self",
                                            through="SkillEdge",
                                            symmetrical=False,
                                            related_name="related_to")
    topological_order = models.PositiveIntegerField(blank=True, null=True)
    objects = SkillManager()

    class Meta:
        # Order skills by their topological order
        ordering = ['topological_order']

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


# SkillEdge model - edges that connect Skill nodes in the knowledge DAG
class SkillEdge(models.Model):
    parent_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="parent_skills")
    child_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="children_skills")
    same_subject = models.BooleanField(default=True)
    ''' Currently defunct, to add this in later...
    relatedness = models.DecimalField(decimal_places=2,
                                      max_digits=3,
                                      default=1,
                                      validators=[MaxValueValidator(1), MinValueValidator(0)])
    '''

    def __str__(self):
        return self.parent_skill.name + " -> " + self.child_skill.name

    def save(self, *args, **kwargs):
        if self.parent_skill.subject == self.child_skill.subject:
            setattr(self, 'same_subject', True)
        else:
            setattr(self, 'same_subject', False)
        super(SkillEdge, self).save(*args, **kwargs)


# Kahn's algorithm, updates topological order of skills in each skill tree after Skilledge save or delete
@receiver(post_save, sender=SkillEdge, dispatch_uid='save_update_topological_order')
@receiver(post_delete, sender=SkillEdge, dispatch_uid='delete_update_topological_order')
def update_topological_order(sender, instance, **kwargs):
    def parent_edges_of_child(skill_obj, edge_list):
        # Receives Skill object and list of SkillEdge objects
        # Returns list of SkillEdge objects that are parent edges of the skill_obj argument
        filtered = list(filter(lambda x: x.child_skill == skill_obj, edge_list))
        return filtered

    # subject - subject area of the graph being topologically sorted
    # edges - all SkillEdge objects connecting to skills with parent_skill__subject=child_skill__subject=subject
    # root_nodes - all Skill objects in the subject area with no parents
    subject = instance.parent_skill.subject
    edges = list(SkillEdge.objects.filter(parent_skill__subject=subject, same_subject=True))
    root_nodes = []
    for i in Skill.objects.filter(subject=subject):
        if not i.get_parent_skills():
            root_nodes.append(i)
    j = 0

    # Assigning topological order
    while root_nodes:
        node = root_nodes.pop()
        setattr(node, 'topological_order', j)
        node.save()
        j += 1
        for edge in edges[:]:
            if edge.parent_skill == node:
                child = edge.child_skill
                edges.remove(edge)
                edges_with_child = parent_edges_of_child(child, edges)
                if not edges_with_child:
                    root_nodes.append(child)

    # Calls subject method that repopulates the topological dependency matrix
    subject.repopulate_dependency_matrix()

    # Updates topological orders if skilledge changed when same_subject=False
    # Same code, but updates other_subject dependency matrix and skill topological orders
    if not instance.same_skill:
        other_subject = instance.child.subject
        edges = list(SkillEdge.objects.filter(parent_skill__subject=other_subject, same_subject=True))
        root_nodes = []
        for i in Skill.objects.filter(subject=other_subject):
            if not i.get_parent_skills():
                root_nodes.append(i)
        j = 0

        # Assigning topological order
        while root_nodes:
            node = root_nodes.pop()
            setattr(node, 'topological_order', j)
            node.save()
            j += 1
            for edge in edges[:]:
                if edge.parent_skill == node:
                    child = edge.child_skill
                    edges.remove(edge)
                    edges_with_child = parent_edges_of_child(child, edges)
                    if not edges_with_child:
                        root_nodes.append(child)
        other_subject.repopulate_dependency_matrix()
