#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python vehicle_vault/manage.py collectstatic --no-input
python vehicle_vault/manage.py migrate
python vehicle_vault/manage.py seed_data



