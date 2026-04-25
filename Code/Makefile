# ---- Variables ----
VENV = env
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
FLAKE = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy

FOLDER_CONFIG = Configs
SCRIPT = a_maze_ing.py 
CONFIG = config.txt
REQ = $(FOLDER_CONFIG)/requirements.txt
MARKER=$(VENV)/.installed 

all: install lint-strict run

install: $(MARKER)

$(MARKER): $(REQ)
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating a new virtual env..."; \
		python3 -m venv $(VENV); \
	fi 
	@echo "Installing/Updating project dependencies..."
	@$(PIP) install -r $(REQ)
	@touch $(MARKER)
 
		
run: install lint
	@echo "Start A_MAZE_ING in a virtual env..."
# open a new window and run the Maze_Generation
	@gnome-terminal --window --maximize -- bash -c "$(PY) $(SCRIPT) $(CONFIG)"

debug: install
	@echo  "Start debuging the Maze Generator"
	@$(PY) -m pdb $(SCRIPT) $(CONFIG)

clean:
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@echo "Cleaning all project cache files..."
# 1. Finds and deletes all __pycache__ folders anywhere
	@find . -type d -name "__pycache__" -exec rm -rf {} +
# 2. Deletes lingering compiled python files anywhere
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
# 3. Recursively removes Mypy and Pytest cache folders anywhere
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "Project directory is completely clean!"

lint: install
	@echo "Running lint flake8..."
	@$(FLAKE) --exclude=env . && echo "Flake8 is [OK]!"
	@echo "Running mypy"
	@$(MYPY) --exclude env --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict: install
	@echo "Running lint flake8 ."
	@$(FLAKE) --exclude=env .
	@echo "Running mypy"
	@$(MYPY) --exclude env --strict .

.PHONY: install run debug clean lint lint-strict