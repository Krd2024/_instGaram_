FROM python:3.11-alpine

# RUN apt-get update && apt-get install -y python3 python3-pip 
RUN apk add --no-cache bash
WORKDIR /django_app

COPY requirements.txt /django_app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /django_app

EXPOSE 8000

# Применение миграций перед запуском сервера (опционально)
# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
