FROM python:3.11.0

LABEL maintainer="Reza Teymouri Nejad <rezatn0934@gmail.com>" \
      description="Dockerfile for a Python application using Python 3.11" \
      version="1.0" \
      source="https://github.com/rezatn0934/RSS-Feed-Aggregator.git"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY . /code/

CMD python3 main.py
