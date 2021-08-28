build:
	isort parsifal
	black parsifal
	flake8 parsifal
	./manage.py makemigrations --check --dry-run --settings=parsifal.test_settings
