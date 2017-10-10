PYTHON:=python3

SRC:=todo
VENV:=venv

ROOT:=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))# https://stackoverflow.com/a/23324703
SRC:=$(ROOT)$(SRC)
VENV:=$(ROOT)$(VENV)

PYTHON:=$(VENV)/bin/python3

HOST:=0.0.0.0
PORT:=5000
run: venv
	FLASK_APP=todo/__init__.py $(VENV)/bin/flask run --host=$(HOST) --port=$(PORT)

venv:
	virtualenv $(VENV)
	$(VENV)/bin/pip install -U pip
	$(VENV)/bin/pip install -Ur requirements.txt
