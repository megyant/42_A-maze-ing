PYTHON = python3
SRC = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint flake8 mypy lint-strict mypy-strict

install:
	$(PYTHON) -m pip install flake8 mypy

run:
	$(PYTHON) $(SRC) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SRC) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache

lint: flake8 mypy

flake8:
	-$(PYTHON) -m flake8 .

mypy:
	-$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: flake8 mypy-strict

mypy-strict:
	-$(PYTHON) -m mypy . --strict