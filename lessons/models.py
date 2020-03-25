from os.path import basename
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from skills.models import Skill


class Lesson(models.Model):
    # lesson_title - charfield of lesson title
    # slug - lesson_title uniquely slugified, populated after save() is called
    # lesson_text - html template of lesson, uploaded to media/lessons
    # skill - one-to-one relationship to Skill model
    lesson_title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    lesson_text = models.FileField(upload_to='lessons')
    skill = models.OneToOneField(Skill, on_delete=models.CASCADE, related_name='lesson')

    class Meta:
        order_with_respect_to = 'skill'

    def __str__(self):
        return self.lesson_title

    def get_absolute_url(self):
        return reverse('lessons:lesson', args=[self.slug])

    # populates slug field with slugified lesson_title after save() is called
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.lesson_title)
        super(Lesson, self).save(*args, **kwargs)

    def html_filename(self):
        return basename(self.lesson_text.name)
