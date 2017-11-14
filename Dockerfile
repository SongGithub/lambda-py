FROM python:alpine3.6

MAINTAINER song.jin

RUN apk update && apk add bash

ADD . /app/

WORKDIR /app/

RUN pip install -r requirements.txt

