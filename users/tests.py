from django.test import TestCase
from .models import CustomUser


class UserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(username='testuser_1',
                                  password='testuser_password',
                                  email='testuser@testmail.com',
                                  age=20)

    def test_user_existence(self):
        user = CustomUser.objects.get(username='testuser_1')
        self.assertTrue(user)
