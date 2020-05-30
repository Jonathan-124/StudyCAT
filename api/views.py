from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import F
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from curricula.models import Curriculum
from curricula.serializers import CurriculumSerializer
from units.models import Unit
from units.serializers import UnitSerializer
from lessons.models import Lesson
from lessons.serializers import LessonSerializer
from skills.models import Skill
from userprofiles.models import Skillfulness, CurrentlyStudying
from userprofiles.serializers import CurrentlyStudyingSerializer
from questions.models import Question
from questions.serializers import QuestionSerializer
from .serializers import PostTestUpdateSerializer, PostPlacementBulkUpdateSerializer, UnitReviewUpdateSerializer, CurrentlyStudyingUpdateSerializer


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
        prerequisite_data = []
        incomplete_start_skills = Skillfulness.objects.filter(user_profile=user_profile, skill__in=curriculum.start_skills, skill_level=0).prefetch_related('skill')
        ancestors = set()
        for i in incomplete_start_skills:
            ancestors.update(i.skill.ancestor_ids)
        ancestors = list(ancestors)
        incomplete_prerequisites = Skillfulness.objects.filter(user_profile=user_profile, skill__in=ancestors, skill_level=0).prefetch_related('skill__lesson')
        for i in incomplete_prerequisites:
            prerequisite_data.append(LessonSerializer(i.skill.lesson).data)
        curriculum_status = user_profile.curriculum_units_completion_percentage(curriculum)
        currently_studying = CurrentlyStudying.objects.filter(user_profile=user_profile, curriculum=curriculum)
        if currently_studying:
            return Response({"curriculum_status": curriculum_status, "prerequisite_data": prerequisite_data, "test_date": currently_studying[0].test_date})
        else:
            return Response({"curriculum_status": curriculum_status, "prerequisite_data": prerequisite_data})


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
        obj = Curriculum.objects.get(id=kwargs.get('pk'))
    except ObjectDoesNotExist:
        return Response({"message": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        start_pack = []
        end_pack = []
        for i in obj.start_skills:
            random_question = Question.objects.random(i)
            serialized_question = QuestionSerializer(random_question).data
            start_pack.append(serialized_question)
        for i in obj.end_skills:
            random_question = Question.objects.random(i)
            serialized_question = QuestionSerializer(random_question).data
            end_pack.append(serialized_question)
        return Response({"start_skills_questions": start_pack, "end_skills_questions": end_pack})


@api_view()
@login_required()
def get_unit_review_question_pack(request, *args, **kwargs):
    question_pack = []
    user_profile = request.user.profile
    lessons = Unit.objects.get(id=kwargs.get('pk')).lessons.all()
    to_be_tested = Skillfulness.objects.filter(user_profile=user_profile, skill__lesson__in=lessons, skill_level__gt=0).prefetch_related('skill')
    for i in to_be_tested:
        random_question = Question.objects.random(i.skill.id)
        serialized_question = QuestionSerializer(random_question).data
        question_pack.append(serialized_question)
    return Response(question_pack)


# Receives post request with a JSON object {"skill_pk": int, "score": decimal of average correctness of responses}
# Updates user skill_level for the skill id, as well as its ancestors/descendants based on the user's current score
@api_view(['PATCH'])
@login_required()
def post_test_update(request, *args, **kwargs):
    user_profile = request.user.profile
    serializer = PostTestUpdateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            skillfulness = Skillfulness.objects.get(user_profile=user_profile, skill__id=request.data["skill_pk"])
        except ObjectDoesNotExist:
            return Response({"message": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["score"] > 0.6:
                user_profile.last_lesson_completion = timezone.now()
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
@api_view(['PATCH'])
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
        Skillfulness.objects.filter(user_profile=user_profile, skill__id__in=to_be_updated, skill_level__lt=3).update(skill_level=F('skill_level') + 1)
        return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@login_required()
def unit_review_update(request, *args, **kwargs):
    user_profile = request.user.profile
    serializer = UnitReviewUpdateSerializer(data=request.data)
    if serializer.is_valid():
        correct_to_be_updated = set()
        incorrect_to_be_updated = set()
        correct_skill_objs = Skill.objects.filter(id__in=request.data["correct_skill_ids"])
        incorrect_skill_objs = Skill.objects.filter(id__in=request.data["incorrect_skill_ids"])
        for i in correct_skill_objs:
            ancestors = i.ancestor_ids
            correct_to_be_updated.add(i.id)
            correct_to_be_updated.update(set(ancestors))
        for i in incorrect_skill_objs:
            descendants = i.descentant_ids
            incorrect_skill_objs.add(i.id)
            incorrect_skill_objs.update(set(descendants))
        user_profile.last_lesson_completion = timezone.now()
        Skillfulness.objects.filter(user_profile=user_profile, skill__id__in=correct_to_be_updated,
                                        skill_level__lt=3).update(skill_level=F('skill_level') + 1)
        Skillfulness.objects.filter(user_profile=user_profile, skill__id__in=incorrect_to_be_updated,
                                        skill_level__gt=0).update(skill_level=F('skill_level') - 1)
        return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get request that returns two serialized lists
# 1st list is all of request.user's currently studying objects, 2nd list is list of all other valid curriculum objects
# untested for empty querysets
@api_view()
@login_required()
def get_profile_update_data(request, *args, **kwargs):
    user_profile = request.user.profile
    currently_studying_objs = CurrentlyStudying.objects.filter(user_profile=user_profile)
    valid_curricula_objs = Curriculum.objects.exclude(id__in=currently_studying_objs.values_list('curriculum__id', flat=True))
    serialized_currently_studying_objs = CurrentlyStudyingSerializer(currently_studying_objs, many=True).data
    serialized_valid_curricula_objs = CurriculumSerializer(valid_curricula_objs, many=True).data
    return Response({"currently_studying": serialized_currently_studying_objs, "curricula": serialized_valid_curricula_objs}, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required()
def create_currently_studying(request, *args, **kwargs):
    user_profile = request.user.profile
    serializer = CurrentlyStudyingUpdateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            curriculum_obj = Curriculum.objects.get(id=request.data["curriculum"])
            if "test_date" in request.data:
                CurrentlyStudying.objects.create(user_profile=user_profile, curriculum=curriculum_obj,
                                                 test_date=request.data["test_date"])
            else:
                CurrentlyStudying.objects.create(user_profile=user_profile, curriculum=curriculum_obj)
        except:
            return Response({"message": "Unable to create object"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@login_required()
def update_currently_studying(request, *args, **kwargs):
    user_profile = request.user.profile
    serializer = CurrentlyStudyingUpdateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            currently_studying_obj = CurrentlyStudying.objects.get(user_profile=user_profile, curriculum=request.data["curriculum"])
            if "test_date" in request.data:
                currently_studying_obj.test_date = request.data["test_date"]
            else:
                currently_studying_obj.test_date = None
            currently_studying_obj.save(update_fields=["test_date"])
        except ObjectDoesNotExist:
            return Response({"message": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@login_required()
def delete_currently_studying(request, *args, **kwargs):
    user_profile = request.user.profile
    serializer = CurrentlyStudyingUpdateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            currently_studying_obj = CurrentlyStudying.objects.get(user_profile=user_profile, curriculum=request.data["curriculum"])
            currently_studying_obj.delete()
        except ObjectDoesNotExist:
            return Response({"message": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "success"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
