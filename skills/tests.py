from django.test import TestCase
from .models import Skill, SkillEdge
import decimal


class SkillTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Skill.objects.create(name='testskill_1')
        Skill.objects.create(name='testskill_2')
        Skill.objects.create(name='testskill_3')
        Skill.objects.create(name='testskill_4')
        SkillEdge.objects.create(parent_skill=Skill.objects.get(id=1),
                                 child_skill=Skill.objects.get(id=2),
                                 relatedness=0.4)
        SkillEdge.objects.create(parent_skill=Skill.objects.get(id=3),
                                 child_skill=Skill.objects.get(id=4),
                                 relatedness=0.1)

    def test_skill_existence(self):
        first_skill = Skill.objects.get(id=1)
        name = first_skill.name
        self.assertEquals(name, 'testskill_1')

    def test_skilledge_existence(self):
        first_edge = SkillEdge.objects.get(id=1)
        first_parent_skill = first_edge.parent_skill
        first_child_skill = first_edge.child_skill
        self.assertEquals(first_parent_skill, Skill.objects.get(id=1))
        self.assertEquals(first_child_skill, Skill.objects.get(id=2))
        self.assertEquals(first_edge.relatedness, decimal.Decimal('0.4'))

    def test_skill_deletion_skilledge_status(self):
        Skill.objects.get(id=4).delete()
        self.assertQuerysetEqual(SkillEdge.objects.all(),
                                 SkillEdge.objects.filter(id=1),
                                 transform=lambda x: x)

    def test_skilledge_deletion_skill_status(self):
        SkillEdge.objects.get(id=2).delete()
        self.assertTrue(Skill.objects.all().filter(id=4).exists())

    def test_get_children_skills(self):
        self.assertQuerysetEqual(Skill.objects.get(id=1).get_children_skills(),
                                 Skill.objects.filter(id=2),
                                 transform=lambda x: x)

    def test_get_parent_skills(self):
        self.assertQuerysetEqual(Skill.objects.get(id=2).get_parent_skills(),
                                 Skill.objects.filter(id=1),
                                 transform=lambda x: x)
