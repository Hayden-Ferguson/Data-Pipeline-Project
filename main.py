import psycopg2
import csv
import json
import sys
from config import load_config

#Exact details of database undecided
def create_tables():
    commands = (
        """
        CREATE TABLE placeholder(
        
        )
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def read_csv(filename):
    with open(filename, mode ='r') as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            print(lines)

def read_json(filename):
    with open(filename, mode ='r') as file:
        data = json.load(file)
        print(json.dump(data))

def fill_database(value_list):
    sql = "INSERT INTO placeholder(value) VALUES(%s) RETURNING *" #Change when database details decided
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.executemany(sql, value_list)

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    #create_tables()    Not yet applicable
    if(len(sys.argv)>1):
        read_csv(sys.argv[1])