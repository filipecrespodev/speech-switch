FROM python:3.7

RUN apt update -y && apt install -y ffmpeg 

ENV  PYTHONUNBUFFERED 1
RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /data/
