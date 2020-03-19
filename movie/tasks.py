import logging
from collections import OrderedDict
from itertools import islice

from django.contrib.auth.models import User

from core.clients.cache.client import cache_client
from core.models import CeleryResult
from movie.models import Movie
from movierecommender.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def process_suggest_for_user(self, user_id):
    user = User.objects.filter(pk=user_id).first()
    if not user:
        return

    cache_client.delete(user_id)

    # Terminate all pending tasks of user
    pending_tasks = list(user.celeryresult_set.filter(status=CeleryResult.PENDING).values_list('task_id', flat=True))
    if pending_tasks:
        app.control.revoke(task_id=pending_tasks, terminate=True)
        CeleryResult.objects.filter(task_id__in=pending_tasks).update(status=CeleryResult.CANCELLED)

    # time.sleep(10)
    if not isinstance(user, User):
        return

    following_genres = user.genrefollow_set.select_related('genre').all()
    following_artist = user.artistfollow_set.select_related('artist').all()
    following_movies = user.moviefollow_set.select_related('movie').prefetch_related('movie__cast',
                                                                                     'movie__genres').all()

    movie_list = OrderedDict()
    counter = 0
    for i in Movie.objects.prefetch_related('cast', 'genres').exclude(
            pk__in=following_movies).iterator():
        print(counter)

        score = 0
        artists = i.cast.all()
        genres = i.genres.all()

        for genre_follow in following_genres:
            if genre_follow.genre in genres:
                score += 5
        for artist_follow in following_artist:
            if artist_follow.artist in artists:
                score += 2
        for moviefollow in following_movies:
            for genre in moviefollow.movie.genres.all():
                if genre in genres:
                    score += 0.2
            for artist in moviefollow.movie.cast.all():
                if artist in artists:
                    score += 0.1
        if score:
            setattr(i, 'score', score)
            movie_list[i.dataset_id] = score
        counter += 1
    movie_list = {k: v for k, v in sorted(movie_list.items(), key=lambda item: item[1], reverse=True)}
    first_10 = list(islice(movie_list, 10))

    # set celery task status to completed
    CeleryResult.objects.filter(task_id=self.request.id).update(status=CeleryResult.COMPLETED)

    # set cache client
    cache_client.set(user_id, first_10)
