import ast
import csv
import os

import django

from movie.models import Movie, Artist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movierecommender.settings')

django.setup()

with open('movie/datasets/credits.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')
    next(reader, None)  # skip headers
    for row in reader:
        cast = ast.literal_eval(row[0])
        movie_id = row[-1]
        movie_instance = Movie.objects.filter(dataset_id=movie_id).first()
        if not movie_instance:
            continue

        artists = []
        for role in cast:
            artist, _ = Artist.objects.get_or_create(dataset_id=role['id'], defaults={'name': role['name']})
            artists.append(artist.id)

        movie_instance.cast.add(*artists)
