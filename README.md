# Тестовое задание 

Портал для проведения online турнира по решению математических задач

## Используемые технологии

1. Python3.5
1. Django 1.11
1. rest_framework
1. Celery 4.0 (брокер rabbitMQ)
1. PostgreSQL

## Установка и запуск

Создать виртуальное окружение:
```bash
    mkvirtualenv math_tasks
    workon math_tasks
```

Установить зависимости:
```
    pip install -r requirements.txt
```

Создать базу данных и пользователя:
```bash
    sudo -u postgres psql
    psql
    CREATE DATABASE database_name;
    CREATE USER database_user WITH PASSWORD 'database_password';
    GRANT ALL PRIVILEGES ON DATABASE database_name TO database_user;
    \q
```

В settings.py изменить настройки БД:
```python
    DATABASES = {
    ....
        'NAME': 'database_name',
        'USER': 'database_user',
        'PASSWORD': 'database_password',
    ....
    }
```

Установить миграцию:
```bash
    python manage.py migrate
```

Создать супер пользователя:
```bash
    python manage.py createsuperuser
```

Запустить сервер:
```bash
    python manage.py runserver
```