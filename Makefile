.PHONY: lint format type test ci release verify-release
lint:
	ruff check .
format:
	ruff format .
type:
	mypy

test:
	pytest
ci: lint type test
release:
	python scripts/build_release.py

verify-release:
	cd dist && sha256sum -c SHA256SUMS
