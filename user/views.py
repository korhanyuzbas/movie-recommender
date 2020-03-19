from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.clients.cache.client import cache_client
from core.models import CeleryResult
from movie.models import Movie
from movie.tasks import process_suggest_for_user
from user.serializers import UserSerializer, UserSuggestionSerializer, PasswordChangeSerializer


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        Token.objects.create(user=request.user)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)


class UserRegisterView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer


class UserMeView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        object = self.request.user
        self.check_object_permissions(self.request, object)
        return object


class PasswordChangeView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        object = self.request.user
        self.check_object_permissions(self.request, object)
        return object

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": [_("Wrong password.")]}, status=status.HTTP_400_BAD_REQUEST)
            object.set_password(serializer.data.get("new_password"))
            object.save()
            return Response(UserSerializer(object).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSuggestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        cached_suggestions = cache_client.get(user.id)

        if not cached_suggestions:
            # Do not run task if user not following anything
            if not user.moviefollow_set.exists() or user.artistfollow_set.exists() or user.genrefollow_set.exists():
                return Response({'message': 'no follow, please follow something'}, status=status.HTTP_200_OK)

            task_id = process_suggest_for_user.apply_async(kwargs={'user_id': user.id})
            CeleryResult.objects.create(user_id=user.id, task_id=task_id, status=CeleryResult.PENDING)
            return Response({'message': 'is in progress'}, status=status.HTTP_200_OK)

        qs = Movie.objects.filter(dataset_id__in=cached_suggestions)
        qs = sorted(qs, key=lambda x: cached_suggestions.index(x.dataset_id))
        return Response(UserSuggestionSerializer(qs, many=True).data, status=status.HTTP_200_OK)
