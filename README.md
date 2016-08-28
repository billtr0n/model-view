# pyOrogeny
simple web-database to store and display dynamic rupture simulations from sord. initial start for fully web-based dynamic rupture simulation platform.


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

make database migrations (only run when necessary)<br>
``` python manage.py makemigrations ```<br>

migrate database (only run when necessary)<br>
``` python manage.py migrate ``` <br>

start django server <br>
``` python manage.py runserver ``` <br>


### Todo
* try catch block for unique together models
* query newest distinct figures
* no bounding box around figure
* add support for gmpe comparisons

#### Future
* develop datastore to store raw data
* interactive plotting in client (angular?,d3)





