from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from core.clients.cache.client import cache_client


class SuggestionAbstractModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from movie.tasks import process_suggest_for_user
        process_suggest_for_user.apply_async(kwargs={'user_id': self.user.id})

    def delete(self, *args, **kwargs):
        cache_client.delete(self.user.id)
        super().delete(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class GenreFollow(SuggestionAbstractModel):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Artist(models.Model):
    dataset_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return "{}".format(self.name)


class ArtistFollow(SuggestionAbstractModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Movie(models.Model):
    dataset_id = models.IntegerField(unique=True)
    imdb_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=500)
    genres = models.ManyToManyField(Genre, blank=True)
    cast = models.ManyToManyField(Artist, blank=True)

    def __str__(self):
        return "{} ({})".format(self.title, self.imdb_id)


class MovieFollow(SuggestionAbstractModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
