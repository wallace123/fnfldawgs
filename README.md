# fnfldawgs

Django app for fnfldawgs www.fnfldawgs.com

# Development

Fork the project on github and git clone your fork, e.g.:

```
git clone https://github.com/<username>/fnfldawgs.git
```

Create a virtualenv using Python3 and install dependencies. I develop on Ubuntu so the steps below apply to my development environment. Modify for your operating system as appropriate.

```
$ python3 -m venv myvenv
pip install -r requirements.txt
```
Install postgresql and set up database. See https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04 for postgresql installation and database set up. When creating the database, name it fnfldawgs.

```
From psql
CREATE DATABASE fnfldawgs;
\q
python manage.py migrate
```

Set environment variables as needed. You can add them to .bashrc or myvenv/bin/activate file.

```
export DJANGO_DEBUG=1
export DJANGO_ENABLE_SSL=0
export MY_DJANGO_DB = 1
export DB_USER="<psql_username>"
export DB_PASS="<psql_password>"
```

Check code style

```
pylint --load-plugins pylint_django fnfl/
```

Run the development server

```
python manage.py runserver
```

# Deployment

This project is already set up for deployment to Heroku, on the app fnfldawgs.

The Heroku app has the following addons:

```
heroku addons:create heroku-postgresql
heroku addons:create ssl
```
Heroku config variables that are set:

```
DATABASE_URL: <database url>
DJANGO_DEBUG: 0
DJANGO_SECRET_KEY: <secret key value>
```

TODO:
* I put items to work in the issues

