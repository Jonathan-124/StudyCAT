from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.text import slugify


class Subject(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    dependencies = ArrayField(ArrayField(models.IntegerField(), default=list), default=list)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)

    # Repopulates dependency/adjacency matrix of subject graph, see Skill receiver w/ Kahn's algorithm
    # Called after topological order changed; IMPORTANT: assumes skills ordered by topological order
    def repopulate_dependency_matrix(self):
        dependency_matrix = []
        num_skills = self.skills.count()
        for skill in self.skills.all():
            parent_ids = skill.get_parent_skills().values_list('topological_order', flat=True)
            adjacency_row = [0] * num_skills
            for i in parent_ids:
                adjacency_row[i] = 1
            dependency_matrix.append(adjacency_row)
        setattr(self, 'dependencies', dependency_matrix)
        self.save()
