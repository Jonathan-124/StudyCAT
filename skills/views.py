from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Skill
from questions.models import Question
from questions.serializers import QuestionSerializer


# Receives get request with kwarg 'pk', retrieves random question with skill_id = pk
# Returns response of JSON object containing serialized question (JSON) and user_skill (decimal [0, 1])
@api_view()
def skill_based_randomizer(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        skill_id = kwargs.get('pk')
        user_profile = request.user.profile
        user_skill_lvl = user_profile.get_skill_level(skill_id)
        random_question = Question.objects.random(skill_id)
        serialized_question = QuestionSerializer(random_question).data
        return Response({"skill_id": skill_id, "question": serialized_question,
                         "user_skill": user_skill_lvl})


# Receives get request with kwarg 'pk', retrieves num random questions with skill_id = pk
# Returns response of JSON object containing serialized questions (list length num)
@api_view()
def skill_question_pack(request, num=3, *args, **kwargs):
    skill_id = kwargs.get('pk')
    skill_topological_order = Skill.objects.get(id=skill_id).topological_order
    questions = Question.objects.random_questions(skill_id, num)
    pack = []
    for i in questions:
        serialized_question = QuestionSerializer(i).data
        pack.append(serialized_question)
    return Response({"questions": pack, "topological_order": skill_topological_order})


# Receives get request with kwarg 'pk', retrieves one question for each parent skill of skill whose id=pk
# Returns response of JSON object containing JSON objects of parent skill_ids and serialized questions
@api_view()
def parent_skill_question_pack(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        parent_skills = Skill.objects.get(id=kwargs.get('pk')).get_parent_skills()
        pack = []
        for i in parent_skills:
            skill_id = i.id
            question = i.questions.random(skill_id)
            serialized_question = QuestionSerializer(question).data
            pack.append({"skill_id": skill_id, "question": serialized_question})
        return Response({"questions": pack})


# Receives get request with kwarg 'pk', retrieves one question for each child skill of skill whose id=pk
# Returns response of JSON object containing JSON objects of child skill_ids and serialized questions
@api_view()
def children_skill_question_pack(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        children_skills = Skill.objects.get(id=kwargs.get('pk')).get_children_skills()
        pack = []
        for i in children_skills:
            skill_id = i.id
            question = i.questions.random(skill_id)
            serialized_question = QuestionSerializer(question).data
            pack.append({"skill_id": skill_id, "question": serialized_question})
        return Response({"questions": pack})


# Receives two lists of topological orders, returns lesson data response
@api_view()
def get_lesson_data_from_topological_order(request, *args, **kwargs):
    if request.user.is_anonymous:
        return Response({"message": "You are not logged in"}, status=status.HTTP_403_FORBIDDEN)
    else:
        terminal_lessons_data = Skill.objects.get_lesson_data(request.query_params.getlist("terminal_ids"))
        next_lessons_data = Skill.objects.get_lesson_data(request.query_params.getlist("next_skills"))
        return Response({"terminal_lessons_data": terminal_lessons_data, "next_lessons_data": next_lessons_data})
