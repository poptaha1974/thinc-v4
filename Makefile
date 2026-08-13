.PHONY: lint format type test ci
lint:
	ruff check .
format:
	ruff format .
type:
	mypy

test:
	pytest
ci: lint type test
