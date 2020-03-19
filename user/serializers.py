from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from movie.models import Movie


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'token',
            'password',
            'last_login',
            'first_name',
            'last_name',
            'date_joined',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')
        try:
            password_validation.validate_password(password)
        except Exception as e:
            raise ValidationError(e)
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    def get_token(self, user):
        token = Token.objects.get(user=user)
        return token.key


class UserSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'imdb_id')


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
