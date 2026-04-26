# Variables
PYTHONPATH := src
PYTEST := PYTHONPATH=$(PYTHONPATH) pytest
RUFF := ruff
STREAMLIT := streamlit

.PHONY: help test lint format clean cov cov-html run requirements benchmark stress-test

help:
	@echo "Available commands:"
	@echo "  make test          Run all unit tests"
	@echo "  make lint          Run ruff linter"
	@echo "  make format        Run ruff formatter"
	@echo "  make cov           Run tests with coverage report"
	@echo "  make cov-html      Run tests and generate HTML coverage report"
	@echo "  make run           Run the Streamlit dashboard locally"
	@echo "  make requirements  Export dependencies to requirements.txt"
	@echo "  make benchmark     Run performance metrics on production data"
	@echo "  make stress-test   Generate 1M rows and run stress benchmarks"
	@echo "  make clean         Remove python cache files"

test:
	$(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

cov:
	PYTHONPATH=$(PYTHONPATH) pytest --cov=src --cov-report=term-missing

cov-html:
	PYTHONPATH=$(PYTHONPATH) pytest --cov=src --cov-report=html
	@echo "Report generated in htmlcov/index.html"

run:
	PYTHONPATH=$(PYTHONPATH) $(STREAMLIT) run main.py

requirements:
	uv export --format requirements-txt > requirements.txt

benchmark:
	PYTHONPATH=$(PYTHONPATH) pytest tests/performance/test_efficiency.py -s

stress-test:
	python tests/performance/data_generator.py 1000000
	STRESS_TEST=1 PYTHONPATH=$(PYTHONPATH) pytest tests/performance/test_efficiency.py -s

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov data/stress_test.csv
