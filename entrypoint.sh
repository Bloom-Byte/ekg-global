#! /bin/bash
python manage.py migrate 
python manage.py collectstatic --noinput 
python manage.py update_rates --schedule --latest --cron "0 * * * *"
python manage.py runserver 0.0.0.0:8000
