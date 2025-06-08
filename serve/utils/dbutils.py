from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from utils.config import DATABASE_URL


# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_data_from_db(query: str, value: str) -> List[Dict[str, Any]]:
    """
    Executes a parameterized SQL query and returns the results as dictionaries.

    Args:
        query (str): SQL query with a named parameter :value.
        value (str): Value to be bound to :value.

    Returns:
        List[Dict[str, Any]]: Query results as list of dictionaries.
    """
    with SessionLocal() as session:
        result = session.execute(text(query), {"value": value})
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]