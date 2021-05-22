FROM python:3.8-slim

ENV PYTHONIOENCODING utf-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US:

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
