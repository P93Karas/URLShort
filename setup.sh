#!/bin/bash
set -e

echo "=== Setting up Python environment ==="

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Created virtual environment in ./venv"
fi

source venv/bin/activate

pip install --upgrade pip

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "Installed dependencies from requirements.txt"
else
    echo "requirements.txt not found!"
    exit 1
fi

echo "Applying migrations..."
python manage.py migrate


echo "Starting Django development server at http://127.0.0.1:8000/"
python manage.py runserver
