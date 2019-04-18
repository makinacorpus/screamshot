FROM python:3.5

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y libx11-xcb1 libxrandr2 libasound2 \
    libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libnss3 libxss1

RUN mkdir screamshot
WORKDIR /screamshot

COPY ./requirement.txt /screamshot

RUN pip3 install -r requirement.txt
RUN pip3 install pylint
RUN pip3 install mypy
RUN pip3 install requests

RUN useradd -ms /bin/bash default
USER default
