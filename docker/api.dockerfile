FROM python:3.8

# Environment (API and PUBLIC)
ENV PROJECT_ROOT /home/movierecommender

COPY ./requirements.txt $PROJECT_ROOT/
RUN pip install -r $PROJECT_ROOT/requirements.txt

ADD ./src $PROJECT_ROOT/src/

ENV PYTHONPATH $PROJECT_ROOT/
ENV PYTHONPATH $PROJECT_ROOT/src
ENV DJANGO_SETTINGS_MODULE movierecommender.settings

WORKDIR $PROJECT_ROOT

RUN mkdir logs
RUN mkdir logs/uwsgi

EXPOSE 8082
