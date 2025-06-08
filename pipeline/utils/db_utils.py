import re
import logging
from utils.connection_utils import connect_to_postgres, ensure_database_exists, ensure_schema_exists
from src.schema import tables
from psycopg2.extensions import cursor as Cursor
from typing import List, Set

def table_exists(cursor: Cursor, schema_name: str, table_name: str) -> bool:
    """
    Check if a table exists within a specific schema.

    Args:
        cursor (Cursor): Database cursor.
        schema_name (str): The schema where the table should reside.
        table_name (str): Name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = %s AND table_schema = %s
        );
        """,
        (table_name, schema_name),
    )
    return cursor.fetchone()[0]


def get_existing_columns(cursor, schema_name, table_name):
    """Retrieves the existing columns of a table."""
    cursor.execute(
        """
        SELECT LOWER(column_name)
        FROM information_schema.columns
        WHERE table_name = %s AND table_schema = %s;
        """,
        (table_name, schema_name),
    )
    return {row[0] for row in cursor.fetchall()}

def get_existing_columns(cursor: Cursor, schema_name: str, table_name: str) -> Set[str]:
    """
    Retrieve the list of column names in a given table.

    Args:
        cursor (Cursor): Database cursor.
        schema_name (str): Schema name.
        table_name (str): Table name.

    Returns:
        Set[str]: Set of existing column names in lowercase.
    """
    cursor.execute(
        """
        SELECT LOWER(column_name)
        FROM information_schema.columns
        WHERE table_name = %s AND table_schema = %s;
        """,
        (table_name, schema_name),
    )
    return {row[0] for row in cursor.fetchall()}

def parse_table_schema(table_schema: str) -> List[str]:
    """
    Parse the raw table schema string into a list of column definitions.

    Supports complex types and ignores inline comments.

    Args:
        table_schema (str): Raw schema string.

    Returns:
        List[str]: Cleaned list of column definitions.
    """
    cleaned_lines = []
    for line in table_schema.split("\n"):
        line = line.split("--")[0].strip()
        if line:
            cleaned_lines.append(line)

    cleaned_schema = " ".join(cleaned_lines)

    # Split on commas not within parentheses (e.g., NUMERIC(10,2))
    pattern = re.compile(r",(?!(?:[^()]*\([^()]*\))*[^()]*\))")
    columns = pattern.split(cleaned_schema)

    return [col.strip() for col in columns if col.strip()]


def update_table(cursor: Cursor, schema_name: str, table_name: str, table_schema: str) -> None:
    """
    Add new columns or drop missing ones based on schema diff.

    Args:
        cursor (Cursor): DB cursor.
        schema_name (str): Schema name.
        table_name (str): Table to update.
        table_schema (str): New schema definition.
    """
    full_table_name = f"{schema_name}.{table_name}"
    existing_columns = get_existing_columns(cursor, schema_name, table_name)
    new_columns = parse_table_schema(table_schema)
    new_column_names = {col.split()[0].lower() for col in new_columns}

    # Add new columns
    for col_definition in new_columns:
        col_name = col_definition.split()[0].lower()
        if col_name not in existing_columns:
            cursor.execute(f"ALTER TABLE {full_table_name} ADD COLUMN {col_definition};")
            logging.info(f"Added column '{col_name}' to table '{full_table_name}'.")

    # Drop obsolete columns
    for col_name in existing_columns:
        if col_name not in new_column_names:
            cursor.execute(f"ALTER TABLE {full_table_name} DROP COLUMN {col_name};")
            logging.info(f"Dropped column '{col_name}' from table '{full_table_name}'.")

    logging.info(f"Table '{full_table_name}' updated successfully.")


def create_or_update_table(table_name: str, table_schema: str, schema_name: str = "data") -> None:
    """
    Create a new table or update the existing one using schema definition.

    Args:
        table_name (str): Table name.
        table_schema (str): Schema string.
        schema_name (str, optional): Schema name. Defaults to "data".
    """
    conn = connect_to_postgres()
    cursor = conn.cursor()

    try:
        ensure_schema_exists(cursor, schema_name)
        full_table_name = f"{schema_name}.{table_name}"

        logging.info(f"Creating/updating table '{full_table_name}'.")

        if table_exists(cursor, schema_name, table_name):
            update_table(cursor, schema_name, table_name, table_schema)
        else:
            cursor.execute(f"CREATE TABLE {full_table_name} ({table_schema});")
            logging.info(f"Table '{full_table_name}' created successfully.")

        conn.commit()
    except Exception as e:
        logging.error(f"Error creating/updating table '{table_name}': {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def create_tables_in_postgres(tables: dict = tables) -> None:
    """
    Create or update all tables defined in the schema module.

    Args:
        tables (dict): Dictionary containing table definitions.
    """
    ensure_database_exists()
    for table_key in tables:
        table_info = tables[table_key]
        create_or_update_table(
            table_name=table_info["name"],
            table_schema=table_info["schema"],
            schema_name="data"
        )


def setup_db() -> None:
    """
    Entry point for initializing all tables.
    Can be called once during pipeline or app startup.
    """
    create_tables_in_postgres()


def insert_records(table_name: str, records: list):
    if not records:
        return

    conn = connect_to_postgres()
    cursor = conn.cursor()

    for record in records:
        cols = ', '.join(record.keys()).lower()
        vals = tuple(record.values())
        placeholders = ', '.join(['%s'] * len(vals))

        insert_query = f"""
            INSERT INTO data.{table_name} ({cols})
            VALUES ({placeholders})
            ON CONFLICT (id) DO NOTHING;
        """
        cursor.execute(insert_query, vals)

    conn.commit()
    cursor.close()
    conn.close()