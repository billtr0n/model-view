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
* add editable div to input figure captions and simulation comments
* implement visualization of model overview
* clean up model detail page and simulation list
* implement tagging system for database
* add support for gmpe comparisons
* and wave-propagation simulations

#### Future
* develop datastore to store raw data
*





