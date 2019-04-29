FROM python:3.5

RUN apt update
RUN pip3 install flask

RUN mkdir server
WORKDIR /server

COPY ./tests/server /server

EXPOSE 5000
