#!/bin/bash
set -e

# Add this for testing capabilities.
#     ALTER USER $DB_USER CREATEDB;

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $DB_NAME;
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
    ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
    ALTER ROLE $DB_USER SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
    GRANT ALL ON SCHEMA public TO $DB_USER;
EOSQL
