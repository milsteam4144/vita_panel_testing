# Makefile for VITA Panel Testing Project
# Provides convenient commands for development workflow

.PHONY: help install install-dev test test-unit test-integration coverage lint format type-check security clean docs serve dev-server

# Default target
help:
	@echo "VITA Panel Testing - Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup Commands:"
	@echo "  install        Install production dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  setup-dev      Complete development environment setup"
	@echo ""
	@echo "Code Quality Commands:"
	@echo "  format         Format code with black and isort"
	@echo "  lint           Run flake8 linting"
	@echo "  type-check     Run mypy type checking"
	@echo "  security       Run bandit security analysis"
	@echo "  quality        Run all code quality checks"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test           Run all tests"
	@echo "  test-unit      Run unit tests only"
	@echo "  test-integration  Run integration tests only"
	@echo "  coverage       Run tests with coverage report"
	@echo ""
	@echo "Development Commands:"
	@echo "  serve          Start development server"
	@echo "  docs           Generate documentation"
	@echo "  clean          Clean up build artifacts"
	@echo ""
	@echo "Scrum/CI Commands:"
	@echo "  pre-commit     Run all pre-commit hooks"
	@echo "  validate       Full validation pipeline (quality + tests)"

# Python and pip executables (adjust for your virtual environment)
PYTHON := python
PIP := pip
PRE_COMMIT := pre-commit

# Installation commands
install:
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r dev-requirements.txt
	$(PRE_COMMIT) install

setup-dev:
	$(PYTHON) setup_dev_env.py

# Code formatting
format:
	@echo "🎨 Formatting code..."
	black src tests vita_app.py auth.py file_uploader.py llm_connect.py
	isort src tests vita_app.py auth.py file_uploader.py llm_connect.py
	@echo "✅ Code formatting complete"

# Linting
lint:
	@echo "🔍 Running linting..."
	flake8 src tests vita_app.py auth.py file_uploader.py llm_connect.py
	@echo "✅ Linting complete"

# Type checking
type-check:
	@echo "🔬 Running type checking..."
	mypy src vita_app.py auth.py file_uploader.py llm_connect.py
	@echo "✅ Type checking complete"

# Security analysis
security:
	@echo "🔒 Running security analysis..."
	bandit -r src vita_app.py auth.py file_uploader.py llm_connect.py
	safety check
	@echo "✅ Security analysis complete"

# Combined code quality
quality: format lint type-check security
	@echo "✅ All code quality checks complete"

# Testing commands
test:
	@echo "🧪 Running all tests..."
	$(PYTHON) -m pytest
	@echo "✅ Tests complete"

test-unit:
	@echo "🧪 Running unit tests..."
	$(PYTHON) -m pytest tests/unit -v
	@echo "✅ Unit tests complete"

test-integration:
	@echo "🧪 Running integration tests..."
	$(PYTHON) -m pytest tests/integration -v
	@echo "✅ Integration tests complete"

coverage:
	@echo "📊 Running tests with coverage..."
	$(PYTHON) -m pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated"

# Development server
serve:
	@echo "🚀 Starting VITA development server..."
	panel serve vita_app.py --port 8501 --allow-websocket-origin=localhost:8501 --show --dev

# Documentation
docs:
	@echo "📚 Generating documentation..."
	cd docs && make html
	@echo "✅ Documentation generated"

# Pre-commit hooks
pre-commit:
	@echo "🔧 Running pre-commit hooks..."
	$(PRE_COMMIT) run --all-files
	@echo "✅ Pre-commit hooks complete"

# Full validation pipeline
validate: quality test
	@echo "✅ Full validation pipeline complete"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	@echo "✅ Clean up complete"

# Development workflow shortcuts
dev-check: format lint type-check test-unit
	@echo "✅ Quick development check complete"

ci-check: quality test coverage
	@echo "✅ CI/CD validation complete"