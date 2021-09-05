# Parsifal

Parsifal is a tool to support researchers to perform systematic literature reviews.

A systematic literature review is a secondary study with the objective to identify, analyze and interpret all available evidences from primary studies related to a specific research question. As suggested by Kitchenham and Charters, the activity to perform a systematic literature review involves planning, conducting and reporting the review.

Performing a systematic literature review is a labor-intensive task that requires a huge amount of work from the researcher, designing the protocol, adjusting the search string, filtering the results, sometimes more than a thousand of articles, selecting those articles that attends the include criteria and removing those articles that attends the exclude criteria. After that, the researcher might start to analyze the relevant result one by one.

# Specs

The project is currently running on the following versions:

* Python 3.9
* Django 3.2
* PostgreSQL 12
* Bootstrap 3.4
* jQuery 3.6

# Running Locally

To run the project locally first you need to clone the repository:

```
git clone https://github.com/vitorfs/parsifal.git
```

Create a virtualenv:

```
virtualenv venv -p python3
```

Install the development requirements:

```
pip install -r requirements/local.txt
```

Now you should either setup a local PostgreSQL database or use SQLite.

Create a `.env` file in the project root (you can create one by making a copy of the `.env.example`):

```
cp .env.example .env
```

Now add the `DATABASE_URL` with the connection string pointing to your local database:

```
DATABASE_URL=postgres://richardwagner:holygrail@localhost:5432/parsifal
```

Or for SQLite:

```
DATABASE_URL=sqlite:////tmp/parsifal.sqlite3
```

Or if you want to place it elsewhere:

```
DATABASE_URL=sqlite:////Users/vitor/dev/parsifal/parsifal.sqlite3
```

Now run the migrations:

```
python manage.py migrate
```

Run the local server:

```
python manage.py runserver
```

# License

The source code is released under the [MIT License](https://github.com/vitorfs/parsifal/blob/master/LICENSE).
