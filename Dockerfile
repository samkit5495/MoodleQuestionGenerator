FROM python:3.10
LABEL project="moodlequestiongenerator"

ENV PYTHONUNBUFFERED=1
WORKDIR /moodlequestiongenerator
COPY requirements.txt ./
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
COPY ./ ./