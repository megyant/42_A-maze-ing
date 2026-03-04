VENV    = venv
PYTHON  = $(VENV)/bin/python3
PIP     = $(VENV)/bin/pip


SRC     = a_maze_ing.py
CONFIG  = config.txt

.PHONY: install run debug clean fclean lint flake8 mypy lint-strict mypy-strict

all: install run

all_clean: install run clean

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy

run:
	$(PYTHON) $(SRC) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SRC) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache $(VENV)

fclean: clean
	rm -rf output_maze.txt

lint: flake8 mypy

flake8:
	-$(PYTHON) -m flake8 .

mypy:
	-$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: flake8 mypy-strict

mypy-strict:
	-$(PYTHON) -m mypy . --strict



# Alterations:
# - Added venv to the whole thing, hopefully will work
# - added fclean and all - if we run make all or just make will install and run
# - added all_clean to run and clean installation and cache files