import os
import psycopg2
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import os
from dotenv import load_dotenv

def load_env_vars():
    """Loads environment variables and returns them as a dict."""
    load_dotenv()
    return {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
    }

def get_pg_connection(dbname=None):
    """Returns a psycopg2 connection using .env credentials and optional dbname override."""
    env = load_env_vars()
    try:
        conn = psycopg2.connect(
            dbname=dbname or env["dbname"],
            user=env["user"],
            password=env["password"],
            host=env["host"],
            port=env["port"]
        )
        logging.info(f"Connected to PostgreSQL database: {dbname or env['dbname']}")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to PostgreSQL: {e}")
        return None

def connect_to_postgres():
    """Connects to the default PostgreSQL database from .env."""
    return get_pg_connection()

def ensure_database_exists(db_name="prod"):
    """Ensures the specified database exists; creates it if not."""
    conn = get_pg_connection("postgres")  # Connect to default 'postgres' DB
    if conn is None:
        return

    try:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,)
        )
        exists = cursor.fetchone()
        if exists:
            logging.info(f"Database '{db_name}' already exists.")
        else:
            cursor.execute(f"CREATE DATABASE {db_name}")
            logging.info(f"Database '{db_name}' created.")

        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to ensure database existence: {e}")


def ensure_schema_exists_and_create(schema_name="data"):
    """Ensures that the specified schema exists in the database. If not, creates it."""
    try:
        conn = connect_to_postgres()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s",
            (schema_name,),
        )
        if not cursor.fetchone():
            cursor.execute(f"CREATE SCHEMA {schema_name}")
            logging.info(f"Schema '{schema_name}' created.")
        else:
            logging.info(f"Schema '{schema_name}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to ensure schema existence: {e}")


def ensure_schema_exists(cursor, schema_name):
    """Ensures that a specific schema exists in the database."""
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")