web: gunicorn movierecommender.wsgi --log-file -
worker: celery worker --app=movierecommender -l info --without-gossip --without-mingle --without-heartbeat
