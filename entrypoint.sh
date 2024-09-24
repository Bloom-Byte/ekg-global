#! /bin/bash
python manage.py migrate 
python manage.py collectstatic --noinput 
python manage.py update_rates # Fetches and updates to last 30days stock rates. Populates db with stocks if they do not exist
python manage.py update_rates --schedule --latest --cron "*/5 * * * *" # Schedule background task to update stocks rate to latest rate every 1hr
python manage.py index_stocks # Update stocks' indices
python manage.py runserver 0.0.0.0:8000
python manage.py qcluster &
