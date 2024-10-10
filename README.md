![Python Versions](https://img.shields.io/pypi/pyversions/Django.svg)
# Пет-проект: Платформа для обмена фотографиями

## Описание
Платформа ориентирована на обмен фотографиями между пользователями. Это социальная сеть, где каждый может делиться моментами своей жизни через публикации и взаимодействовать с контентом других пользователей.

## Основные функции

- **Лайки, комментарии и сообщения**: ключевые инструменты взаимодействия с контентом. Пользователи могут оценивать и обсуждать фотографии.
- **Взаимная подписка**: при подписке друг на друга пользователи автоматически добавляются в список друзей, что упрощает взаимодействие и обмен контентом.

Эта платформа предлагает простой и удобный способ оставаться на связи через фотографии.

# Технические детали:

## Установка

1.Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Krd2024/_instGaram_.gi
```
2.Создание виртуального окружения
```bash
   python -m venv .venv
```
3.Активация виртуального окружения
```bash
   .venv\Scripts\activate
```
4.Установка зависимостей проекта
```bash
   pip install -r requirements.txt
```
**Сгенерировать SECRET_KEY в Django**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
**Сосдать файл .env**
Добавьте соответствующие значения в .env файл:
```python
SECRET_KEY = см. выше
```
5.Запуск
```bash
   python manage.py runserver
```
