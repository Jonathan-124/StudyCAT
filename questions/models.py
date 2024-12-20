from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.aggregates import Count
from skills.models import Skill
from random import sample, randint


# Additional manager methods for Question model QuerySets
class QuestionManager(models.Manager):
    # Retrieves random question with question.skill__id=skill_id
    def random(self, skill_id):
        queryset = self.filter(skill__id=skill_id)
        count = queryset.aggregate(count=Count('id'))['count']
        if count == 0:
            return self.none()
        else:
            random_index = randint(0, count - 1)
            return queryset.all()[random_index]

    # Retrieves random question with given topological_order, subject slug
    def random_by_topological_order(self, topological_order, slug):
        queryset = self.filter(skill__subject__slug=slug, skill__topological_order=topological_order)
        count = queryset.aggregate(count=Count('id'))['count']
        if count == 0:
            return self.none()
        else:
            random_index = randint(0, count - 1)
            return queryset.all()[random_index]

    # Retrieves num random questions related to skill with skill_id
    def random_questions(self, skill_id, num):
        queryset = self.filter(skill__id=skill_id)
        count = queryset.aggregate(count=Count('id'))['count']
        if count == 0:
            return self.none()
        elif num > count:
            num = count
        random_index_list = sample(range(0, count), num)
        random_questions = []
        for i in random_index_list:
            random_questions.append(queryset.all()[i])
        return random_questions


# Returns /{subject_slug}/question_images/{question_id}/{filename} path to store the question prompt image
def prompt_image_directory_path(instance, filename):
    return '{0}/question_images/{1}/{2}'.format(instance.skill.subject.slug, instance.id, filename)


# Returns /{subject_slug}/question_images/{question_id}/answer_images/{answer_id}/{filename} path to store answer image
def answer_image_directory_path(instance, filename):
    return '{0}/question_images/{1}/answer_images/{2}/{3}/'.format(instance.question.skill.subject.slug,
                                                               instance.question.id, instance.id, filename)


def get_default_permitted_fields():
    return ["fraction"]


# Question model
# skill - question objects have a many-to-one relationship to skill objects
# question_type - choice of what type of question/what type of input it requires
# question_prompt - plaintext of question prompt, includes KaTeX delimiters
# prompt_image - one-to-one relationship to image associated with question (if exists)
# is_mastery - whether the question is considered a 'mastery' question for the associated skill (currently unused)
# discrimination - how well a question discriminates users who know/don't know a skill (currently unused)
# pseudochance - how likely the user is able to guess the correct answer to the question (current defaults for choice questions)
class Question(models.Model):
    MULTIPLE_CHOICE = 'MC'
    MULTIPLE_SELECTION = 'MS'
    IMAGE_CHOICE = 'IC'
    NUMERICAL_INPUT = 'NI'
    FUNCTION_INPUT = 'FI'
    MATRIX_INPUT = 'MI'
    INTERVAL_INPUT = 'II'

    QUESTION_TYPES = [
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (MULTIPLE_SELECTION, 'Multiple Selection'),
        (IMAGE_CHOICE, 'Image Choice'),
        (NUMERICAL_INPUT, 'Numerical Input'),
        (FUNCTION_INPUT, 'Function Input'),
        (MATRIX_INPUT, 'Matrix Input'),
        (INTERVAL_INPUT, 'Interval Input'),
    ]

    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name='questions')
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    question_prompt = models.TextField()
    permitted_symbols = ArrayField(models.CharField(max_length=32), blank=True, null=True, default=get_default_permitted_fields)
    prompt_image = models.ImageField(null=True, blank=True, upload_to=prompt_image_directory_path)
    is_mastery = models.BooleanField(default=False)
    discrimination = models.DecimalField(decimal_places=3,
                                         max_digits=4,
                                         default=1,
                                         validators=[MaxValueValidator(2), MinValueValidator(0)])
    pseudochance = models.DecimalField(decimal_places=3,
                                       max_digits=4,
                                       default=0,
                                       validators=[MaxValueValidator(1), MinValueValidator(0)])
    objects = QuestionManager()

    def save(self, *args, **kwargs):
        if self.question_type == 'MC' or 'IC':
            try:
                setattr(self, 'pseudochance', 1 / self.answers.count())
            except:
                setattr(self, 'pseudochance', 0.25)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.skill.id) + '-' + self.question_prompt


# Answer model
# answer_text - if Question type MC, plaintext that includes KaTeX delimiters; if IC, image caption; else asciimath
# answer_image - one-to-one relationship to image associated with answer (if exists)
# question - many-to-one foreignkey relation to Questions model
# answer_explanation - plaintext explanation of answer input that includes KaTeX delimiters (if exists)
# answer_correctness - decimal [0, 1] of how correct the associated answer object is
class Answer(models.Model):
    answer_text = models.TextField(null=True, blank=True)
    answer_image = models.ImageField(null=True, blank=True, upload_to=answer_image_directory_path)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers')
    answer_explanation = models.TextField(null=True, blank=True)
    answer_correctness = models.DecimalField(decimal_places=3,
                                             max_digits=4,
                                             default=0,
                                             validators=[MaxValueValidator(1), MinValueValidator(0)])

    def __str__(self):
        return self.answer_text
