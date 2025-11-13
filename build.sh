#!/usr/bin/env bash
# Exit on error
set -o errexit

# Create static files directory if it doesn't exist
mkdir -p staticfiles

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser if it doesn't exist (optional, remove in production)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@maishauni.com').exists() or User.objects.create_superuser('admin@maishauni.com', 'adminpassword')" | python manage.py shell || true

# Collect static files
python manage.py collectstatic --noinput