# EKG Global

## Quick Setup Guide

- Clone the repository

- Change directory to the repository

- Install the requirements using `pip install -r requirements.txt`

- Copy the config in .env.example to a new file called .env and update the values

- Run migrations using `python manage.py migrate`

- Collect staticfiles using `python manage.py collectstatic`

- Create a superuser using `python manage.py createsuperuser`

- Run the server using `python manage.py runserver`

> This project uses a postgres database.++

## With Docker

Run `docker compose up` to start the services
