import graphene

from graphene_django.types import DjangoObjectType

from movie.models import Movie, Genre, Artist


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class GenreType(DjangoObjectType):
    class Meta:
        model = Genre


class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist


class Query(object):
    all_artists = graphene.List(ArtistType)
    all_genres = graphene.List(GenreType)
    all_movies = graphene.List(MovieType)

    def resolve_all_artists(self, info, **kwargs):
        return Artist.objects.all()

    def resolve_all_genres(self, info, **kwargs):
        return Genre.objects.all()

    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.prefetch_related('cast', 'genres').all()
