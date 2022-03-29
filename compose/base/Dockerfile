# syntax=docker/dockerfile:1
FROM python:3
RUN echo "Docker File is running"
RUN pip install --upgrade pip

RUN addgroup --system group
RUN adduser --system --system user --ingroup group
USER user:group

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt .
#
RUN pip install -r requirements.txt

COPY . .
WORKDIR /app

RUN echo "Build complete"