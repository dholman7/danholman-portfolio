.PHONY: install lint test fmt

install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

lint:
	. .venv/bin/activate && ruff check .

fmt:
	. .venv/bin/activate && black .

test:
	. .venv/bin/activate && pytest -q
