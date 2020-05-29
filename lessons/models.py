from os.path import basename
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class LessonManager(models.Manager):
    # Receives list of topological order ids, returns querysets of lessons with skill__topological_order in list
    def get_lessons_from_topological_orders(self, topological_order_list):
        return self.filter(skill__topological_order__in=topological_order_list)


# Lesson model
# lesson_title - charfield of lesson title
# slug - lesson_title uniquely slugified, populated after save() is called
# lesson_text - html template of lesson, uploaded to media/lessons
# skill - one-to-one relationship to Skill model
class Lesson(models.Model):
    lesson_title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    lesson_text = models.FileField(upload_to='lessons')
    skill = models.OneToOneField('skills.Skill', on_delete=models.CASCADE, related_name='lesson')
    objects = LessonManager()

    class Meta:
        order_with_respect_to = 'skill'

    def __str__(self):
        return self.lesson_title

    def get_absolute_url(self):
        return reverse('lessons:lesson', args=[self.slug])

    # populates slug field with slugified lesson_title after save() is called
    def save(self, *args, **kwargs):
        self.slug = slugify(self.lesson_title)
        super(Lesson, self).save(*args, **kwargs)

    def html_filename(self):
        return basename(self.lesson_text.name)


def lesson_image_directory_path(instance, filename):
    return '{0}/lesson_images/{1}/{2}'.format(instance.lesson.skill.subject.name, instance.lesson.slug, filename)


# LessonImage model - manytoone images related to a Lesson object
class LessonImage(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=False, blank=False, upload_to=lesson_image_directory_path)
    caption = models.CharField(null=True, blank=True, max_length=128)
