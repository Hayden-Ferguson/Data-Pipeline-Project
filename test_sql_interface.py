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
    #TODO: Check table structure

def test_fill_database():
    if sql_interface.table_exists("test"):
        sql_interface.drop_table("test")
    sql_interface.create_tables("test")
    input_list = [['1', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5']]
    #input_list gotten from data
    insert, update = sql_interface.fill_database(input_list, "test")
    assert insert == 1
    assert update == 0
    insert, update = sql_interface.fill_database(input_list, "test")
    assert insert == 0
    assert update == 1
    sql_interface.drop_table("test") #assume this works because of later test


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