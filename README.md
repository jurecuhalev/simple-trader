Example Application to help with introduction to Django Testing
===

Instalation
---

If you need to setup your basic python environment:

	sudo apt-get install python-pip python-virtualenv python-dev

From inside simple-trader folder, create new virtualenv:

	virtualenv env

	source env/bin/activate

	pip install -r requirements.txt

	cd trader

	./manage.py syncdb


Run application
---

	./manage.py runserver 0.0.0.0:8000

Run tests
---

	./manage.py test web

Run coverage.py
---

	coverage run --source='.' ./manage.py test web
	coverage html
	
Then open `index.html` inside `htmlcov/`
