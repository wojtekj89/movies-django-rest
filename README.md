# movies-django-rest

REST API written in Django. Movies database with data pulled from OMDB.

[![Build Status](https://travis-ci.com/wojtekj89/movies-django-rest.svg?branch=master)](https://travis-ci.com/wojtekj89/movies-django-rest) [![Coverage Status](https://coveralls.io/repos/github/wojtekj89/movies-django-rest/badge.svg)](https://coveralls.io/github/wojtekj89/movies-django-rest)

## Getting started

App is hosted [here](http://wjmovies.herokuapp.com/movies/)

## Running locally

### Prerequisites

Install PostgreSQL 9.5+, Python 3.7 and Django 2.1

Create postgres account and write it's name in `src/core/local_settings.py` [(see more)](https://docs.djangoproject.com/en/2.1/ref/settings/#databases) or export it in environment setting `DATABASE_URL` [(see dj-database-url)](https://github.com/kennethreitz/dj-database-url). Example:

```
DATABASE_URL=postgres://user:movies@localhost:5432/movies
```

You could also run SQLite3 database provided by Django Framework but `/top` would not work there.

You need to request for [OMDB API KEY](http://www.omdbapi.com/)and store it in the environment setting `OMDB_API_KEY`. If you don't want to store it in env you have to add it before all `manage.py` and `gunicorn` commands.

## Installation

```
pip install -r requirements.txt
cd src
python manage.py migrate
```

### Running the tests

Running django unit tests:

```
cd src && python manage.py test
```

### Running the server locally using SQLite3

```
cd src && python manage.py runserver
```

### Running the server locally using gunicorn and PostgreSQL database

Remember to set up the database and provide DATABASE_URL before you use this command.

```
gunicorn core.wsgi --log-file=- --pythonpath=src
```

# Supported API Endpoints

## /movies

### GET

Provides a list of all movies stored in the database.
Movies can be searched by title or genre and ordered by title or year of production.
Examples:
`/movies/?search=comedy` for all comedy movies
`/movies/?search=ring` for movies with ring in the title
`/movies/?ordering=title` for all movies ordered by the title

### POST

Creates a new movie in the database. Requires title parameter. Response is a result of the search for the title in OMDB API.

## /comments

### GET

List of all comments available in the database. Optional movie filter by id.
`/comments?movie_id=1` for comments to movie with id = 1 only

### POST

Creates a new comment in the database. Requires movie_id and text parameters.

## /top

### GET

Ranked and sorted list of movies by number of comments in specified date range. Requires start and end parameters with date in `DD-MM-YY` format.
