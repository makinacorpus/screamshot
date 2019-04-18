FROM python:3.5

RUN apt-get update
RUN apt-get upgrade -y
RUN pip3 install flask

RUN mkdir server
WORKDIR /server

COPY ./tests/server /server
