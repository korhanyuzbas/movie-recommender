import csv
import json
import os

import django
from movie.models import Movie, Genre

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movierecommender.settings')

django.setup()
Movie.objects.all().delete()
Genre.objects.all().delete()

with open('movie/datasets/movies_metadata.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, dialect='excel')
    next(reader, None)  # skip headers
    for row in reader:
        is_adult = row[0]
        genres = json.loads(row[3].replace("'", '"'))
        dataset_id = row[5]
        imdb_id = row[6]

        try:
            name = row[20]
        except IndexError:
            name = row[8]

        genres_list = []
        for genre in genres:
            genre, _ = Genre.objects.get_or_create(name=genre['name'])
            genres_list.append(genre)
        try:
            instance = Movie.objects.create(imdb_id=imdb_id, title=name, dataset_id=dataset_id)
            instance.genres.add(*genres_list)
        except Exception as e:
            pass
