from django.db import models
from django.utils.text import slugify


# Subject model
# name - Charfield of model name
# slug - unique slug of subject name
class Subject(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Subject, self).save(*args, **kwargs)
