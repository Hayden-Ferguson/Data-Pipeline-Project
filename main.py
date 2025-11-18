import psycopg2
import csv
import json
import sys
from config import load_config

#Exact details of database undecided
#Creates the tables for the database
def create_tables():
    command = ( #Command to create table. Unsure if all variables should be NOT NULL
        """
        CREATE TABLE employees(
            employee_number SERIAL PRIMARY KEY,
            age INTEGER NOT NULL,
            attrition BOOLEAN DEFAULT FALSE,
            buisness_travel VARCHAR(20) NOT NULL,
            daily_rate INTEGER NOT NULL,
            department VARCHAR(30) NOT NULL,
            distance_from_home INTEGER NOT NULL,
            education INTEGER NOT NULL,
            education_field VARCHAR(30) NOT NULL,
            employee_count INTEGER DEFAULT 1,
            environment_satisfaction INTEGER,
            gender VARCHAR(20),
            hourly_rate INTEGER NOT NULL,
            job_involvement INTEGER,
            job_level INTEGER NOT NULL,
            job_role VARCHAR(30) NOT NULL,
            marital_status VARCHAR(10),
            monthly_income INTEGER NOT NULL,
            monthly_rate INTEGER NOT NULL,
            num_companies INTEGER,
            over_18 BOOLEAN DEFAULT TRUE,
            overtime BOOLEAN DEFAULT FALSE,
            percent_salary_hike INTEGER,
            performance_rating INTEGER,
            relationship_status INTEGER,
            standard_hours INTEGER DEFAULT 80,
            stock_option_level INTEGER,
            total_working_years INTEGER,
            training_time_last_year INTEGER,
            work_life_balance INTEGER,
            years_at_company INTEGER DEFAULT 0,
            years_in_current_role INTEGER DEFAULT 0,
            years_since_last_promotion INTEGER DEFAULT 0,
            years_with_current_manager INTEGER DEFAULT 0
        )
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='employees')") #Determines if a table exists
                if(not cur.fetchone()[0]): #If no row exists, showing the table doesn't exists
                    cur.execute(command)
                    print("Employees table created")
                else:
                    print("Employees table already exists")
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
    create_tables()
    if(len(sys.argv)>1): #If there are parameters to calling the main function
        read_files(sys.argv[1:])