# pyOrogeny
simple web-database to store and display dynamic rupture simulations from sord. 


### Starting development server

start redis server
``` redis-server & ```

test redis server
``` redis-cli ping ```

make database migrations (only run on initial install)
``` python manage.py makemigrations ```

migrate database (only run on initial install)
``` python manage.py migrate ``` 

start django server
``` python manage.py runserver ```





