import sql_interface
import psycopg2
from config import load_config
from psycopg2.extras import execute_values
import pytest # pyright: ignore[reportMissingImports]

def test_table_exists():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE test ()")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    assert sql_interface.table_exists("test") == True
    assert sql_interface.table_exists("nonexistant") == False