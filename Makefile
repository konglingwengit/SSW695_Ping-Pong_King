install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	#python -m pytest -vv --cov=pingponglib tests/*.py
	#python -m pytest --nbval notebook.ipynb


lint:
	#pylint --disable=R,C pingponglib cli web
	export PYTHONPATH=src
	pylint --disable=R,C main.py

all: install lint test
