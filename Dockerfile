FROM ubuntu:16.04

MAINTAINER SHO USHIKUBO
RUN mkdir -p /usr/src/app
ENV APP_ROOT /usr/src/app/
WORKDIR $APP_ROOT

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      apt-utils \
      sudo \
      git \
      vim \
      python3 \
      python3-dev \
      python3-setuptools \
      python3-pip \
      nginx \
      sqlite3 && \
    pip3 install -U pip setuptools && \
    ln -s /www/app/nginx/django_nginx.conf /etc/nginx/sites-enabled/
COPY . $APP_ROOT

# pip install exclude pip, setuptools using requirements.txt
RUN pip3 install -r requirements.txt

# japanese support in bash
RUN apt-get install -y language-pack-ja-base language-pack-ja
ENV LANG=ja_JP.UTF-8

EXPOSE 8000
