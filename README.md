<p align="center">
  <a href="https://parsif.al">
    <img src="https://parsif.al/static/img/dark_grail.svg" alt="Parsifal logo" height="128">
  </a>
</p>

<h3 align="center">Parsifal</h3>

<p align="center">
  Parsifal is a tool to support researchers to perform systematic literature reviews.
  <br>
  <br>
  <a href="https://github.com/vitorfs/parsifal/issues/new">Report bug</a>
  ·
  <a href="https://parsif.al/blog/">Blog</a>
  ·
  <a href="https://parsif.al/help/">Help</a>
</p>

## Status

[![codecov](https://codecov.io/gh/vitorfs/parsifal/branch/master/graph/badge.svg?token=FGjSTTlvuG)](https://codecov.io/gh/vitorfs/parsifal)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

A systematic literature review is a secondary study with the objective to identify, analyze and interpret all available evidence from primary studies related to a specific research question. As suggested by Kitchenham and Charters, the activity to perform a systematic literature review involves planning, conducting, and reporting the review.

Performing a systematic literature review is a labor-intensive task that requires a huge amount of work from the researcher, designing the protocol, adjusting the search string, filtering the results, sometimes more than a thousand articles, selecting those articles that attend the inclusion criteria, and removing those articles that attend the exclude criteria. After that, the researcher might start to analyze the relevant result one by one.

## Tech Stack

The project is currently running on the following versions:

* Python 3.9
* Django 4.1
* PostgreSQL 12
* Bootstrap 3.4
* jQuery 3.6

## Running Locally

To run the project locally first you need to clone the repository:

```bash
git clone https://github.com/vitorfs/parsifal.git
```

Create a virtualenv:

```bash
python3 -m venv venv
```

Active virtualenv:

```bash
source venv/bin/activate
```

Install the development requirements:

```bash
pip install -r requirements/local.txt
```

Now you should either setup a local PostgreSQL database or use SQLite.

Create a `.env` file in the project root (you can create one by making a copy of the `.env.example`):

```bash
cp .env.example .env
```

Now add the `DATABASE_URL` with the connection string pointing to your local database:

```bash
DATABASE_URL=postgres://richardwagner:holygrail@localhost:5432/parsifal
```

Or for SQLite:

```bash
DATABASE_URL=sqlite:////tmp/parsifal.sqlite3
```

Or if you want to place it elsewhere:

```bash
DATABASE_URL=sqlite:////Users/vitor/dev/parsifal/parsifal.sqlite3
```

Now run the migrations:

```bbash
python manage.py migrate
```

Run the local server:

```bash
python manage.py runserver
```

Create super user:

```bash
python manage.py createsuperuser
```

## License

The source code is released under the [MIT License](https://github.com/vitorfs/parsifal/blob/master/LICENSE).
