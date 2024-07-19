#!/bin/bash
cd /usr/src/app || exit

echo "======Waiting for database up======"
while ! curl http://db:5432/ 2>&1 | grep '52'
do
  echo "Waiting....."
  sleep 1
done
echo "Database is up..........."

echo "======Migrating======"
python manage.py migrate

echo "======Starting django server======"
python manage.py runserver 0.0.0.0:8000
