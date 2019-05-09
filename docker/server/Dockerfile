FROM python:3.5

COPY ./tests /tmp

RUN pip3 install flask &&\
    pip3 install pyjwt &&\
    mkdir server &&\
    cp -r /tmp/server/* /server &&\
    rm -r /tmp/* &&\
    groupadd -r screamshot &&\
    useradd --no-log-init -r -g screamshot screamshot &&\
    chown -R screamshot:screamshot /server

WORKDIR /server

EXPOSE 5000
