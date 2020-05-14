from django.db import models
from users.models import CustomUser
from questions.models import Question
from lessons.models import Lesson
from units.models import Unit
from curricula.models import Curriculum


# Bug report model
# reporting_user - user that submitted the report
# report_message - report message submitted by user
class GeneralBugReport(models.Model):
    reporting_user = models.ForeignKey(CustomUser,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='bug_reports')
    report_message = models.TextField(max_length=2000)


# Bug report model for individual question objects, inherits GeneralBugReport
# question - question being reported
# reason - choicefield of why the question was reported
class QuestionBugReport(GeneralBugReport):
    PROMPT_ISSUE = 'PI'
    PARTIAL_CREDIT = 'PC'
    ANSWER_ISSUE = 'AI'
    DISPLAY_ISSUE = 'DI'
    OTHER = 'OT'

    REPORT_REASON = [
        (PROMPT_ISSUE, 'There is something wrong with the question prompt'),
        (PARTIAL_CREDIT, 'My answer deserves partial credit (please write down your answer)'),
        (ANSWER_ISSUE, 'There is something wrong with the answer(s)'),
        (DISPLAY_ISSUE, 'The question is not displaying correctly'),
        (OTHER, 'Other'),
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bug_reports')
    reason = models.CharField(max_length=2, choices=REPORT_REASON)


class LessonBugReport(GeneralBugReport):
    FACTUAL_ISSUE = 'FI'
    TYPOGRAPHICAL_ISSUE = 'TI'
    DISPLAY_ISSUE = 'DI'
    SEQUENCING_ISSUE = 'SI'
    OTHER = 'OT'

    REPORT_REASON = [
        (FACTUAL_ISSUE, 'There is something factually incorrect with the lesson'),
        (TYPOGRAPHICAL_ISSUE, 'There are typos present in the lesson'),
        (DISPLAY_ISSUE, 'The lesson is not displaying correctly'),
        (SEQUENCING_ISSUE, 'There are knowledge gaps between this lesson and previous/subsequent lessons'),
        (OTHER, 'Other'),
    ]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='bug_reports')
    reason = models.CharField(max_length=2, choices=REPORT_REASON)


class UnitBugReport(GeneralBugReport):
    DISPLAY_ISSUE = 'DI'
    OTHER = 'OT'

    REPORT_REASON = [
        (DISPLAY_ISSUE, 'The unit is not displaying correctly'),
        (OTHER, 'Other'),
    ]
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='bug_reports')
    reason = models.CharField(max_length=2, choices=REPORT_REASON)


class CurriculumBugReport(GeneralBugReport):
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='bug_reports')
