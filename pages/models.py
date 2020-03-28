from django.db import models
from users.models import CustomUser
from questions.models import Question


class GeneralBugReport(models.Model):
    reporting_user = models.ForeignKey(CustomUser,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='general_bug_reports')
    report_message = models.TextField(max_length=2000)


class QuestionBugReport(models.Model):
    PROMPT_ISSUE = 'PI'
    ANSWER_ISSUE = 'AI'
    DISPLAY_ISSUE = 'DI'

    REPORT_REASON = [
        (PROMPT_ISSUE, 'There is something wrong with the question prompt.'),
        (ANSWER_ISSUE, 'There is something wrong with the answer(s)'),
        (DISPLAY_ISSUE, 'The question is not displaying correctly'),
    ]
    reporting_user = models.ForeignKey(CustomUser,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='question_bug_reports')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bug_reports')
    reason = models.CharField(max_length=2, choices=REPORT_REASON)
    report_message = models.TextField(max_length=2000)
