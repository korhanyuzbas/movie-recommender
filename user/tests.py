from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from core.tests import TestMixin


class UserTestCase(TestCase, TestMixin):

    def test_user_signup(self):
        user_client = APIClient()
        user_client.default_format = 'json'
        data = self.create_mock_user_data()

        response = user_client.post('/user/register/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {
            'username': 'randomusername',
            'password': 'this_is_a_password1',
            'email': 'user@example.com',

        }
        user = User.objects.create_user(**data)
        Token.objects.create(user=user)
        user_client = APIClient()
        user_client.default_format = 'json'

        data = {
            'username': 'randomusername',
            'password': 'this_is_a_password1'
        }
        response = user_client.post('/user/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_me_get(self):
        user, user_client = self.create_user_and_client()
        response = user_client.get('/user/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], user.username)
