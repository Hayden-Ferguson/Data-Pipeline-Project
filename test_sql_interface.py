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
    sql_interface.drop_table("test") #assume this works because of later test
    assert sql_interface.table_exists("nonexistant") == False

def test_create_tables():
    if sql_interface.table_exists("test"):
        sql_interface.drop_table("test")
    sql_interface.create_tables("test")
    assert sql_interface.table_exists("test") == True #assume this works because of previous test
    sql_interface.drop_table("test") #assume this works because of later test
    #the latter only matters to reduce tables

def test_drop_table():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE test ()")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        
    assert sql_interface.table_exists("test") == True
    sql_interface.drop_table("test")
    assert sql_interface.table_exists("test") == False