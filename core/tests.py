from django.contrib.auth.models import User

from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestMixin:
    @staticmethod
    def create_user_and_client():
        user = User.objects.create_user(
            username=get_random_string(6),
            password=get_random_string(9),
            email=get_random_string(5) + '@example.com'
        )
        Token.objects.create(user=user)

        client = APIClient()
        client.default_format = 'json'
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        return user, client

    @staticmethod
    def create_mock_user_data():
        data = {
            'username': get_random_string(6),
            'password': get_random_string(8),
            'email': get_random_string(5) + '@example.com',
            'first_name': get_random_string(6),
            'last_name': get_random_string(6),
        }
        return data
