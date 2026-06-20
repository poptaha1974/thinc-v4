.PHONY: lint format type test ci
lint:
	ruff check .
format:
	ruff format .
type:
	mypy src

test:
	pytest
ci: lint type test
