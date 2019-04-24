FROM python:3.5

RUN apt update
RUN apt install -y libx11-xcb1 libxrandr2 libasound2 \
    libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libnss3 libxss1

RUN mkdir screamshot
WORKDIR /screamshot

COPY . /screamshot

RUN pip3 install -r requirements.txt
RUN pip3 install -r dev-requirements.txt

RUN apt -y install sudo

RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker

RUN sudo apt-get update

EXPOSE 5000
