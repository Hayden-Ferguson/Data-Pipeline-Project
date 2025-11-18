import psycopg2
import csv
import json
import sys
from config import load_config

#Exact details of database undecided
#Creates the tables for the database
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

#Reads and prints a csv file
def read_csv(filename):
    try:
        with open(filename, mode ='r') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                print(lines)
    except FileNotFoundError:
        print(f"Error: The file {filename} could not be found.")
    except csv.Error as e:
        print(f"Error: Failed to decode csv from the file {filename}: {e}")
    except Exception as e:
        print(f"Error: The following error occured trying to read csv from {filename}: {e}")

#Reads and prints a JSON file
def read_json(filename):
    try:
        with open(filename, mode ='r') as file:
            for line in file:
                data = json.loads(line) #load and loads are for file vs string
                print(json.dumps(data)) #same for dump and dumps
    except FileNotFoundError:
        print(f"Error: The file {filename} could not be found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from the file {filename}: {e}")
    except Exception as e:
        print(f"Error: The following error occured trying to read JSON from {filename}: {e}")

#Takes a list of files, and decides to read them as CSV or JSON files
def read_files(filenames):
    for filename in filenames:
        if filename.endswith(".csv"):
            read_csv(filename)
        elif filename.endswith(".json"):
            read_json(filename)
        else:
            print("Invalid command/file")

#Fills database with values (Currently empty)
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
        read_files(sys.argv[1:])