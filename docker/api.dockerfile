FROM ubuntu:bionic

# Update box
RUN apt-get update -y --force-yes
RUN apt-get upgrade -y --force-yes
RUN apt-get install -y --force-yes python3.6 python3-pip python3-dev
RUN apt-get install -y --force-yes libffi-dev libssl-dev
RUN apt-get install -y --force-yes libjpeg-dev libjpeg8-dev libpng-dev libfreetype6-dev gettext
RUN apt-get install -y --force-yes git supervisor apt-transport-https libmysqlclient-dev
RUN apt-get install -y --force-yes nano build-essential locales

# Set locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

# Environment (API and PUBLIC)
ENV PROJECT_ROOT /home/movierecommender

COPY ./requirements.txt $PROJECT_ROOT/
RUN pip3 install -r $PROJECT_ROOT/requirements.txt

ADD ./src $PROJECT_ROOT/src/

ENV PYTHONPATH $PROJECT_ROOT/
ENV PYTHONPATH $PROJECT_ROOT/src
ENV DJANGO_SETTINGS_MODULE movierecommender.settings

WORKDIR $PROJECT_ROOT

RUN mkdir logs
RUN mkdir logs/uwsgi

EXPOSE 8082
