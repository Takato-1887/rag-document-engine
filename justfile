# justfile — common developer commands for rag-document-engine
# Run `just` alone to see this list of available commands.
# Run `just <command>` to execute one, e.g. `just lint`

# Use PowerShell for all recipes on Windows (no sh dependency)
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# justfile — common developer commands for rag-document-engine
...

# Default recipe: show available commands
default:
    @just --list

# Install all dependencies (prod + dev) and set up pre-commit hooks
install:
    uv sync --all-extras --dev
    uv run pre-commit install

# Run the linter (ruff check)
lint:
    uv run ruff check .

# Auto-fix lint issues where possible
lint-fix:
    uv run ruff check --fix .

# Format code (ruff format)
format:
    uv run ruff format .

# Check formatting without modifying files (used in CI)
format-check:
    uv run ruff format --check .

# Run static type checking
typecheck:
    uv run mypy src/ --ignore-missing-imports

# Run the test suite
test:
    uv run pytest tests/ -v

# Run tests with coverage report
test-cov:
    uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Run all quality checks in sequence (mirrors CI exactly)
check: lint format-check typecheck test
    @echo "All checks passed."

# Run pre-commit hooks against all files manually
precommit:
    uv run pre-commit run --all-files

# Verify environment/config loads correctly
verify-config:
    uv run python scripts/verify_config.py

# Remove caches, build artifacts, and __pycache__ directories
clean:
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .pytest_cache
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .mypy_cache
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .ruff_cache
    Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Rebuild the virtual environment from scratch (nuclear option for env issues)
rebuild-env:
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .venv
    uv venv --python "C:\Users\Priyal\AppData\Local\Python\pythoncore-3.12-64\python.exe"
    uv sync --all-extras --dev
