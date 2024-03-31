#!/bin/bash

read -p "Enter name of migration: " message
docker-compose exec rieltor_api alembic revision --autogenerate -m "$message"