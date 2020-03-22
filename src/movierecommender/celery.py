import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movierecommender.settings')

app = Celery('movierecommender', broker=os.environ.get("REDIS_CONNECTION_URL"))

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
