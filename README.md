# pyOrogeny
simple web-database to store and display dynamic rupture simulations from sord. 


### Starting development server

start redis server
``` redis-server & ```

test redis server
``` redis-cli ping ```

start celery worker (from pyorogeny directory)
``` venv/bin/celery --app=model_database.celeryapp:app worker --loglevel=INFO ```

note: call celery from bin directory in project virtualenv

make database migrations (only run on initial install)
``` python manage.py makemigrations ```

migrate database (only run on initial install)
``` python manage.py migrate ``` 

start django server
``` python manage.py runserver ```





