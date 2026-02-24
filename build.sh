#!/usr/bin/env bash

# simple build script for the Django project
# usage: ./build.sh

set -euo pipefail

# store repository root before changing directories
REPO_ROOT="$(pwd)"

# determine Django project root (look for manage.py)
if [ -f "manage.py" ]; then
    DJ_ROOT="."
elif [ -f "community/manage.py" ]; then
    DJ_ROOT="community"
else
    echo "Error: manage.py not found in . or ./community"
    echo "Make sure you're running this from the repository root."
    exit 1
fi

# ensure virtualenv is active or warn
if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo "Warning: no virtual environment detected. It's recommended to activate one."
fi

# pick a Python executable (try `python` then `python3`)
if command -v python >/dev/null 2>&1; then
    PYTHON=python
elif command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    echo "Error: no python or python3 executable found in PATH."
    echo "Run this script from an environment with Python (e.g. activate your venv)."
    exit 1
fi

# ensure DATABASE_URL is defined for local builds (uses sqlite)
export DATABASE_URL="${DATABASE_URL:-sqlite:///./db.sqlite3}"

# install python dependencies from repository root
if [ -f "$REPO_ROOT/requirements.txt" ]; then
    echo "Installing python packages from requirements.txt..."
    "$PYTHON" -m pip install -r "$REPO_ROOT/requirements.txt"
fi

# change to Django project directory for manage.py commands
cd "$DJ_ROOT"

# apply migrations
echo "Running database migrations..."
"$PYTHON" manage.py migrate

# collect static files
echo "Collecting static files..."
"$PYTHON" manage.py collectstatic --noinput

echo "Build complete."
