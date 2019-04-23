FROM python:3.5

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y libx11-xcb1 libxrandr2 libasound2 \
    libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libnss3 libxss1

RUN mkdir screamshot
WORKDIR /screamshot

COPY . /screamshot

RUN pip3 install -r requirement.txt
RUN pip3 install -r ./docker/checks/checks-requirement.txt
RUN python3 setup.py install

EXPOSE 5000

EXPOSE 5000

RUN apt-get -y install sudo

RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker

RUN sudo apt-get update
