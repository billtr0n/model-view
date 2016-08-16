# pyOrogeny
simple web-database to store and display dynamic rupture simulations from sord. 


### Starting development server

install requirements<br>
``` pip install -r requiements.txt ```<br>

start redis server <br>
``` redis-server & ```

test redis server <br>
``` redis-cli ping ```

start celery worker (from pyorogeny directory) <br>
``` venv/bin/celery --app=model_database.celeryapp:app worker --loglevel=INFO ```
<br>
note: call celery from bin directory in project virtualenv<br>

make database migrations (only run on initial install)<br>
``` python manage.py makemigrations ```<br>

migrate database (only run on initial install)<br>
``` python manage.py migrate ``` <br>

start django server <br>
``` python manage.py runserver ``` <br>


### Todo
* commit models to the database
  * status: sim and parameters good,
  * need to add simulation outputs and inputs
  * add data-product model to store premade figures
* develop datastore to store raw data
* build homepage
* build models overview page
* build details page
* restyle upload page
* add nonexistent required directories





