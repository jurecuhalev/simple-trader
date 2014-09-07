Example Application to help with introduction to Django Testing
===

Instalation
---

Unzip the folder and create new virtualenv:

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