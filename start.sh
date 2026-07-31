#!/usr/bin/env bash
set -o errexit

python vehicle_vault/manage.py migrate
python vehicle_vault/manage.py seed_data
gunicorn --chdir vehicle_vault vehicle_vault.wsgi:application

