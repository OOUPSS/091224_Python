#!/bin/bash
export APP_DB_URL="postgresql+psycopg2://admin_user:super_secret_pass@db_postgres:5432/app_db"
alembic upgrade head