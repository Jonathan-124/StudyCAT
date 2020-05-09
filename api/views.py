import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from curricula.models import Curriculum
from units.models import Unit
from units.serializers import UnitSerializer
from lessons.models import Lesson
from lessons.serializers import LessonSerializer
from skills.models import Skill
from userprofiles.models import Skillfulness
from questions.models import Question
from questions.serializers import QuestionSerializer
from .serializers import PostTestUpdateSerializer, PostPlacementBulkUpdateSerializer


# Returns JSON object of list of serialized lessons and one random question that are both at the user's terminus level
@api_view()
@login_required()
def get_homepage_data(request, *args, **kwargs):
    terminus_data = request.user.profile.retrieve_terminus_lessons()
    serialized_lessons = LessonSerializer(terminus_data[0], many=True).data
    random_question = Question.objects.random(terminus_data[1])
    serialized_question = QuestionSerializer(random_question).data
    return Response({"lessons": serialized_lessons, "question": serialized_question})


# Receives curriculum pk, returns list of JSON objects {"slug": unit slug, "percentage": unit completion percentage}
@api_view()
@login_required()
def get_curriculum_completion_status(request, *args, **kwargs):
    user_profile = request.user.profile
    try:
        curriculum = Curriculum.objects.get(id=kwargs.get('pk'))
    except ObjectDoesNotExist:
        return Response({"message": "Curriculum does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = user_profile.curriculum_units_completion_percentage(curriculum)
        return Response(data)


# Receives unit pk, returns serialized unit data
@api_view()
def get_unit_data(request, *args, **kwargs):
    unit = Unit.objects.get(id=kwargs.get('pk'))
    unit_data = UnitSerializer(unit).data
    if request.user.is_authenticated:
        skill_ids = unit.lessons.all().values_list('skill__id', flat=True)
        user_skill_levels = Skillfulness.objects.filter(user_profile=request.user.profile, skill__id__in=skill_ids).values_list('skill', 'skill_level')
        return Response({"unit_data": unit_data, "user_skill_levels": user_skill_levels})
    else:
        return Response({"unit_data": unit_data})


# Receives skill pk, returns serialized parent lesson data
@api_view()
def get_parent_lessons_data(request, *args, **kwargs):
    parents = Skill.objects.get(id=kwargs.get('pk')).get_parent_skills()
    lessons = Lesson.objects.filter(skill__in=parents)
    serialized_lessons = LessonSerializer(lessons, many=True).data
    if request.user.is_authenticated:
        user_skill_levels = Skillfulness.objects.filter(user_profile=request.user.profile, skill__in=parents).values_list('skill', 'skill_level')
        return Response({"lessons_data": serialized_lessons, "user_skill_levels": user_skill_levels})
    else:
        return Response({"lessons_data": serialized_lessons})


# Receives skill pk and optional num, returns random serialized question (or num list of questions) with given skill pk
@api_view()
def get_random_questions(request, *args, **kwargs):
    if kwargs.get('num'):
        random_questions = Question.objects.random_questions(kwargs.get('pk'), kwargs.get('num'))
        serialized_questions = QuestionSerializer(random_questions, many=True).data
        return Response(serialized_questions)
    else:
        random_question = Question.objects.random(kwargs.get('pk'))
        serialized_question = QuestionSerializer(random_question).data
        return Response(serialized_question)


# Receives relation slug and skill pk, retrieves one question for each related skill whose id=pk
# Relation slug can be "parents" or "children"
@api_view()
@login_required()
def get_related_questions(request, *args, **kwargs):
    try:
        relation_list = ["parents", "children"]
        if kwargs.get('relation') not in relation_list:
            raise ValidationError("Relation does not exist")
        skill = Skill.objects.get(id=kwargs.get('pk'))
    except ValidationError:
        return Response({"message": "Relation does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"message": "Skill does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        related_skill_ids = []
        pack = []
        if kwargs.get('relation') == "parents":
            related_skill_ids.extend(skill.get_parent_skills().values_list('id', flat=True))
        else:
            related_skill_ids.extend(skill.get_children_skills().values_list('id', flat=True))
        while related_skill_ids:
            question = Question.objects.random(related_skill_ids.pop())
            pack.append(QuestionSerializer(question).data)
        return Response(pack)


# Receives two parameters - scope (str) and pk (int)
# scope is a choice of "curriculum", "unit", "refresher"
# pk is the id of scope indicated (with the exception of refresher)
# Returns two lists ("start_skills_questions" and "end_skills_questions") of serialized question objects
@api_view()
@login_required()
def get_placement_question_pack(request, *args, **kwargs):
    try:
        scope_list = ["curriculum", "unit", "refresher"]
        if kwargs.get('scope') not in scope_list:
            raise ValidationError("Scope does not exist")
        obj = None
        if kwargs.get('scope') == "curriculum":
            obj = Curriculum.objects.get(id=kwargs.get('pk'))
        elif kwargs.get('scope') == "unit":
            obj = Unit.objects.get(id=kwargs.get('pk'))
    except ValidationError:
        return Response({"message": "Scope does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"message": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        start_pack = []
        end_pack = []
        start_skills_id_list = []
        end_skills_id_list = []
        if kwargs.get('scope') == "curriculum" or kwargs.get('scope') == "unit":
            start_skills_id_list.extend(json.loads(obj.start_skills)["skill_id_list"])
            end_skills_id_list.extend(json.loads(obj.end_skills)["skill_id_list"])
        else:
            end_skills_id_list.extend(request.user.profile.retrieve_terminus_skills())
        for i in start_skills_id_list:
            random_question = Question.objects.random(i)
            serialized_question = QuestionSerializer(random_question).data
            start_pack.append(serialized_question)
        for i in end_skills_id_list:
            random_question = Question.objects.random(i)
            serialized_question = QuestionSerializer(random_question).data
            end_pack.append(serialized_question)
        return Response({"start_skills_questions": start_pack, "end_skills_questions": end_pack})


# Receives post request with a JSON object {"skill_pk": int, "score": decimal of average correctness of responses}
# Updates user skill_level for the skill id, as well as its ancestors/descendants based on the user's current score
@api_view(['POST'])
@login_required()
def post_test_update(request, *args, **kwargs):
    user_profile = request.user.profile
    serializer = PostTestUpdateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            skillfulness = Skillfulness.objects.get(user_profile=user_profile, skill__id=request.data["skill_pk"])
        except ObjectDoesNotExist:
            Response({"message": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["score"] > 0.6:
                skillfulness.skill.ancestor_ids.append(skillfulness.skill.id)
                Skillfulness.objects.filter(user_profile=user_profile, skill__id__in=skillfulness.skill.ancestor_ids,
                                            skill_level__lt=3).update(skill_level=F('skill_level') + 1)
            else:
                skillfulness.skill.descendant_ids.append(skillfulness.skill.id)
                Skillfulness.objects.filter(user_profile=user_profile, skill__id__in=skillfulness.skill.descendant_ids,
                                            skill_level__gt=0).update(skill_level=F('skill_level') - 1)
            return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Receives post request with a JSON object {"confirmed_correct_skill_ids": list}
# Updates user skill_level all ids in list and their ancestors descendants accordingly
@api_view(['POST'])
@login_required()
def post_placement_bulk_update(request, *args, **kwargs):
    user_profile = request.user.profile
    serializer = PostPlacementBulkUpdateSerializer(data=request.data)
    if serializer.is_valid():
        to_be_updated = set()
        skill_objs = Skill.objects.filter(id__in=request.data["confirmed_correct_skill_ids"])
        for i in skill_objs:
            ancestors = i.ancestor_ids
            to_be_updated.add(i.id)
            to_be_updated.update(set(ancestors))
        Skillfulness.objects.filter(user_profile=user_profile, skill__id__in=to_be_updated).update(skill_level=1)
        return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
