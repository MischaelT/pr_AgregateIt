SHELL := /bin/bash

manage_py := python3 app/manage.py
# Тут не проелы, а табуляция
runserver: 
	$(manage_py) runserver 

migrate:
	$(manage_py) migrate

migrations:
	$(manage_py) makemigrations

shell:
	$(manage_py) shell_plus --print-sql

show_urls:
	$(manage_py) show_urls

worker:
	cd app && celery -A settings worker -l info

beat:
	cd app && celery -A settings beat -l info

superuser:
	$(manage_py) createsuperuser

pytest:
	 pytest ./app/tests/ --cov=app --cov-report html && coverage report --fail-under=74

show-coverage:  ## open coverage HTML report in default browser
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"
