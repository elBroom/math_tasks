# Тестовое задание

[![Build Status](https://travis-ci.com/elBroom/math_tasks.svg?token=cVo8HUojxrnVwNzUccZT&branch=master)](https://travis-ci.com/elBroom/math_tasks)

Портал для проведения online турнира по решению математических задач

## Используемые технологии

1. Python3.5
1. Django 1.11
1. PostgreSQL
1. Redis

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

    # for test
    CREATE DATABASE test_database_name;
    GRANT ALL PRIVILEGES ON DATABASE test_database_name TO database_user;
    ALTER DATABASE test_database_name OWNER TO database_user;
    \q
```


Cкопировать settings_tpl.py и изменить настройки:
```sh
    cp math_tasks/settings_tmp.py math_tasks/settings.py
    vim math_tasks/settings.py
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