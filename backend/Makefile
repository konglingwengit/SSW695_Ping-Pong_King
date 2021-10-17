install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	#python -m pytest -vv --cov=pingponglib tests/*.py
	#python -m pytest --nbval notebook.ipynb
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	python -m pytest 

lint:
	#pylint --disable=R,C pingponglib cli web
	pylint --disable=R,C main.py

all: install lint test
