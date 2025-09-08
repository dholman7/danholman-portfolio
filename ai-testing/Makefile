.PHONY: install lint test fmt

install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

lint:
	. .venv/bin/activate && ruff check .

fmt:
	. .venv/bin/activate && black .

test:
	. .venv/bin/activate && pytest -q

# Generate public-safe artifacts from private sources
redacted:
	. .venv/bin/activate || true; python3 scripts/redact.py ../ai-private ./redacted

# Eval helpers

.PHONY: eval-run
# Dummy eval runner placeholder (user plugs in their call to model)
eval-run:
	@echo "Simulating model output..." > evals/reports/output.txt
	python3 evals/scorers/contains_scoring.py evals/cases/summarize.jsonl evals/reports/output.txt > evals/reports/scores.jsonl
	@echo "Wrote evals/reports/scores.jsonl"
