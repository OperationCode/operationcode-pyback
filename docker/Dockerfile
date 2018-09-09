FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src
RUN mkdir /static

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile* /src/

RUN pipenv install --deploy --system --dev

COPY src /src

EXPOSE 8000
CMD python manage.py collectstatic --no-input;python manage.py makemigrations;python manage.py migrate;gunicorn pyback.wsgi -b 0.0.0.0:8000 -w 3