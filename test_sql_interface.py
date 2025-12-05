import sql_interface
import psycopg2
from config import load_config
from psycopg2.extras import execute_values
import pytest # pyright: ignore[reportMissingImports]

#NOTE: These tests are heavily intertwined, due to using one function to help test another.
# Even if a test passes, the function might be wrong if another test fails.

def test_table_exists():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE test (a INT)")
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
    assert sql_interface.count_rows("test") == 1

    insert, update = sql_interface.fill_database(input_list, "test")
    assert insert == 0
    assert update == 1
    assert sql_interface.count_rows("test") == 1

    #Can handle multiple inputs and inserting while updating
    input_list = [['1', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5'],\
                    ['2', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5']]
    insert, update = sql_interface.fill_database(input_list, "test")
    assert insert == 1
    assert update == 1
    assert sql_interface.count_rows("test") == 2

    #Can handle multiple updates
    input_list = [['1', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5'],\
                    ['2', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5']]
    insert, update = sql_interface.fill_database(input_list, "test")
    assert insert == 0
    assert update == 2
    assert sql_interface.count_rows("test") == 2

    #Can handle multiple inputs
    input_list = [['3', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5'],\
                    ['4', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5']]
    insert, update = sql_interface.fill_database(input_list, "test")
    assert insert == 2
    assert update == 0
    assert sql_interface.count_rows("test") == 4

    sql_interface.drop_table("test") #assume this works because of later test


def test_drop_table():
    sql_interface.create_tables("test")
    assert sql_interface.table_exists("test") == True
    sql_interface.drop_table("test") #table did existed, but no longer exists
    assert sql_interface.table_exists("test") == False

def test_clear_table():
    if sql_interface.table_exists("test"):
        sql_interface.drop_table("test")
    sql_interface.create_tables("test")

    input_list = [['1', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5'],\
                    ['2', '41', 'Yes', 'Travel_Rarely', 'Sales', '1', '2', 'Life Sciences', '2', 'Female', '94', '3', '2',\
                   'Sales Executive', 'Single', '19479', '8', 'Yes', '11', '3', '1', '80', '0', '8', '0', '1', '6', '4', '0', '5']]
    insert, update = sql_interface.fill_database(input_list, "test")
    assert sql_interface.count_rows("test") == 2
    sql_interface.clear_table("test")
    assert sql_interface.count_rows("test") == 0

#Mostly to prove that the debugging function used in other tests works properly
def test_count_rows():
    if sql_interface.table_exists("test"):
        sql_interface.drop_table("test")
    command = (
        '''
        CREATE TABLE "test"(
            a INT,
            b CHAR
        )
        ''')
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                conn.commit()
                assert sql_interface.count_rows("test") == 0
                cur.execute("INSERT INTO test(a, b) VALUES (6, 'a');")
                conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        
    assert sql_interface.count_rows("test") == 1
    sql_interface.drop_table("test")