#!/usr/bin/env bash
set -o errexit

python vehicle_vault/manage.py migrate
gunicorn --chdir vehicle_vault vehicle_vault.wsgi:application
