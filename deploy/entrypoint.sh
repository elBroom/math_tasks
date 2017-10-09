#!/bin/bash -e
SRC=/usr/src/app/deploy
ETC=/etc/app


echo "Copy to ${ETC}/uwsgi.ini..."
cp ${SRC}/uwsgi.ini ${ETC}/uwsgi.ini

echo "Running migrations..."
python3 /usr/src/app/manage.py migrate

echo "Running celery..."
cd /usr/src/app/
celery -A math_tasks worker -l info --logfile=/var/log/app/celery.log 2>/dev/null &

echo "Running command: $@"
exec "$@"
