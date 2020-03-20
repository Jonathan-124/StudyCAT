from django.test import TestCase
from users.models import CustomUser
from .models import UserProfile
from skills.models import Skill
import decimal


class UserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(username='testuser_1',
                                  password='testuser_password',
                                  email='testuser@testmail.com',
                                  age=20)
        Skill.objects.create(name='testskill_1')

    def test_create_user_profile_signal(self):
        profile = UserProfile.objects.get(id=1)
        self.assertTrue(profile)

    def test_autocreate_userskill_signal(self):
        profile = UserProfile.objects.get(id=1)
        self.assertEquals(profile.skills.get(name='testskill_1'), Skill.objects.get(name='testskill_1'))

    def test_userskill_nonexistence_postdelete(self):
        profile = UserProfile.objects.get(id=1)
        Skill.objects.get(name='testskill_1').delete()
        self.assertQuerysetEqual(profile.skills.all(), profile.skills.filter(id=2), transform=lambda x: x)

    def test_create_all_skills(self):
        CustomUser.objects.create(username='testuser_2',
                                  password='testuser_password',
                                  email='testuser2@testmail.com',
                                  age=20)
        profile = UserProfile.objects.get(id=2)
        self.assertTrue(profile)
        self.assertEquals(profile.skills.get(id=1), Skill.objects.get(id=1))

    def test_get_skill_level(self):
        profile = UserProfile.objects.get(id=1)
        testskill_1_skilllevel = profile.get_skill_level(Skill.objects.get(name='testskill_1'))
        self.assertEquals(testskill_1_skilllevel, 0)

    def test_user_skill_after_skill_delete(self):
        Skill.objects.get(name='testskill_1').delete()
        profile = UserProfile.objects.get(id=1)
        with self.assertRaises(Skill.DoesNotExist):
            profile.skills.get(name='testskill_1')

    def test_change_skill_level(self):
        profile = UserProfile.objects.get(id=1)
        profile.change_skill_level(Skill.objects.get(name='testskill_1'), 0.2)
        self.assertEquals(profile.get_skill_level(Skill.objects.get(name='testskill_1')), decimal.Decimal('0.2'))
