from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from movie.models import Movie, Genre, Artist, MovieFollow, ArtistFollow, GenreFollow
from movie.serializers import MovieSerializer, GenreSerializer, ArtistSerializer


class MovieViewSet(ListAPIView, RetrieveAPIView, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = []

    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        instance = Movie.objects.filter(id=pk).first()
        if instance:
            MovieFollow.objects.get_or_create(user=request.user, movie=instance)
            return Response({"status": "OK"})
        else:
            raise ValidationError('Movie not found')

    @action(methods=['post'], detail=True)
    def unfollow(self, request, pk):
        instance = MovieFollow.objects.filter(user=request.user, movie_id=pk).first()
        if not instance:
            raise ValidationError('Object not found')

        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(ListAPIView, RetrieveAPIView, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        movie = Genre.objects.filter(id=pk).first()
        if movie:
            GenreFollow.objects.get_or_create(user=request.user, genre=movie)
            return Response({"status": "OK"})
        else:
            raise ValidationError('Movie not found')

    @action(methods=['post'], detail=True)
    def unfollow(self, request, pk):
        instance = GenreFollow.objects.filter(user=request.user, genre_id=pk).first()
        if not instance:
            raise ValidationError('Object not found')

        return Response(status=status.HTTP_204_NO_CONTENT)


class ArtistViewSet(ListAPIView, RetrieveAPIView, GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        instance = Artist.objects.filter(id=pk).first()
        if instance:
            ArtistFollow.objects.get_or_create(user=request.user, artist=instance)
            return Response({"status": "OK"})
        else:
            raise ValidationError('Movie not found')

    @action(methods=['post'], detail=True)
    def unfollow(self, request, pk):
        instance = ArtistFollow.objects.filter(user=request.user, artist_id=pk).first()
        if not instance:
            raise ValidationError('Object not found')

        return Response(status=status.HTTP_204_NO_CONTENT)
