FROM python:alpine3.6

MAINTAINER song.jin

RUN apk update
RUN apk add --no-cache bash
RUN apk add --no-cache build-base

ADD . /app/

WORKDIR /app/

RUN pip install pandas
RUN pip install -r requirements.txt

