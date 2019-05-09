FROM python:3.5

COPY ./requirements.txt ./dev-requirements.txt /tmp/

RUN apt update &&\
    apt install -y libx11-xcb1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libnss3 \
    libxss1 &&\
    rm -r /var/lib/apt/lists/* &&\
    pip3 install -r /tmp/requirements.txt &&\
    pip3 install -r /tmp/dev-requirements.txt &&\
    rm /tmp/* &&\
    mkdir /screamshot

WORKDIR /screamshot

EXPOSE 5000
