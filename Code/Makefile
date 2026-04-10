# ---- Make Settings ----
SHELL := /bin/bash
.ONESHELL:
# ---- Variables ----
VENV = env
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
FLAKE = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy

FOLDER_CONFIG = Configs
SCRIPT = a_maze_ing.py 
CONFIG = config.txt

all: run


install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating a new virtual env"; \
		python3 -m venv $(VENV); \
		source $(VENV)/bin/activate; \
		echo "Installing project dependencies..."; \
		$(PIP) install -r $(FOLDER_CONFIG)/requirements.txt; \
	fi 
		
run: install
	@echo "Start A_MAZE_ING in a virtual env..."
# open a new window and run the Maze_Generation
	@gnome-terminal --window --maximize -- bash -c "$(PY) $(SCRIPT) $(CONFIG);"


.PHONY: install run debug clean lint lint-strict