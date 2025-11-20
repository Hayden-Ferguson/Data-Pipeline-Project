import psycopg2
import csv
import json
import sys
import re
import os
from config import load_config

#Returns True if the employees table exists, returns False otherwise
def table_exists():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='employees')") #Determines if the employees table exists
                return cur.fetchone()[0]
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

#Creates the table for the sql database
def create_tables():
    command = ( #Command to create table. More standardized names.
        #SERIAL PRIMARY KEY might cause new emplyees to be skipped if they use default SERIAL number. 
        #over_18, daily_rate, monthly_income, and employee_count removed. years_with_curr_manager became years_with_current_manager
        #assume people who do not have all fields filled out are new employees
        #NOTE: Currently inserting Null into fields with DEFAULT
        """
        CREATE TABLE employees(
            employee_number SERIAL PRIMARY KEY,
            age INTEGER NOT NULL CHECK (age > 17),
            attrition BOOLEAN DEFAULT FALSE,
            business_travel VARCHAR(20) NOT NULL,
            department VARCHAR(30) NOT NULL,
            distance_from_home INTEGER CHECK (distance_from_home > -1),
            education INTEGER NOT NULL CHECK (education > 0 AND education < 6),
            education_field VARCHAR(30) NOT NULL,
            environment_satisfaction INTEGER CHECK (environment_satisfaction > 0 AND environment_satisfaction < 6),
            gender VARCHAR(20),
            hourly_rate INTEGER NOT NULL CHECK (hourly_rate > 0),
            job_involvement INTEGER CHECK (job_involvement > 0 AND job_involvement < 6),
            job_level INTEGER NOT NULL CHECK (job_level > 0 AND job_level < 6),
            job_role VARCHAR(30) NOT NULL,
            marital_status VARCHAR(10),
            monthly_rate INTEGER NOT NULL CHECK (monthly_rate > 0),
            num_companies_worked INTEGER CHECK (num_companies_worked > -1),
            overtime BOOLEAN DEFAULT FALSE,
            percent_salary_hike INTEGER DEFAULT 0,
            performance_rating INTEGER CHECK (performance_rating > 0 AND performance_rating < 6),
            relationship_satisfaction INTEGER CHECK (relationship_satisfaction > 0 AND relationship_satisfaction < 6),
            standard_hours INTEGER DEFAULT 80 CHECK (standard_hours > 0),
            stock_option_level INTEGER CHECK (stock_option_level > -1),
            total_working_years INTEGER CHECK (total_working_years > -1),
            training_times_last_year INTEGER CHECK (training_times_last_year > -1),
            work_life_balance INTEGER CHECK (work_life_balance > 0 AND work_life_balance < 6),
            years_at_company INTEGER DEFAULT 0 CHECK (years_at_company > -1),
            years_in_current_role INTEGER DEFAULT 0 CHECK (years_in_current_role > -1),
            years_since_last_promotion INTEGER DEFAULT 0 CHECK (years_since_last_promotion > -1),
            years_with_current_manager INTEGER DEFAULT 0 CHECK (years_with_current_manager > -1)
        )
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if(not table_exists()): #If table doesn't exist
                    cur.execute(command)
                    print("Employees table created")
                else: #Shouldn't happen from main function
                    print("Employees table already exists")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

#Fills database with values given a list of inputs that contain ordered parameters
def fill_database(input_list):
    sql = "INSERT INTO employees(employee_number, age, attrition, business_travel, department, distance_from_home," \
    "education, education_field, environment_satisfaction, gender, hourly_rate, job_involvement, job_level," \
    "job_role, marital_status, monthly_rate, num_companies_worked, overtime, percent_salary_hike, performance_rating," \
    "relationship_satisfaction, standard_hours, stock_option_level, total_working_years, training_times_last_year," \
    "work_life_balance, years_at_company, years_in_current_role, years_since_last_promotion, years_with_current_manager) " \
    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                #print(len(input_list[0]))
                cur.executemany(sql, input_list)

            conn.commit()
            print(f"Employee table updated with {cur.rowcount} rows")
    except (Exception, psycopg2.DatabaseError) as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error: The following error occured trying to insert into the database: {error} on line {exc_tb.tb_lineno}")


"""
For reference:
TABLE employees(
    employee_number SERIAL PRIMARY KEY, 0
    age INTEGER NOT NULL CHECK (age > 17),
    attrition BOOLEAN DEFAULT FALSE,
    business_travel VARCHAR(20) NOT NULL,
    department VARCHAR(30) NOT NULL,
    distance_from_home INTEGER CHECK (distance_from_home > -1), 5
    education INTEGER NOT NULL CHECK (education > 0 AND education < 6),
    education_field VARCHAR(30) NOT NULL,
    environment_satisfaction INTEGER CHECK (environment_satisfaction > 0 AND environment_satisfaction < 6),
    gender VARCHAR(20),
    hourly_rate INTEGER NOT NULL CHECK (hourly_rate > 0), 10
    job_involvement INTEGER CHECK (job_involvement > 0 AND job_involvement < 6),
    job_level INTEGER NOT NULL CHECK (job_level > 0 AND job_level < 6),
    job_role VARCHAR(30) NOT NULL,
    marital_status VARCHAR(10),
    monthly_rate INTEGER NOT NULL CHECK (monthly_rate > 0), 15
    num_companies_worked INTEGER CHECK (num_companies_worked > -1),
    overtime BOOLEAN DEFAULT FALSE,
    percent_salary_hike INTEGER DEFAULT 0,
    performance_rating INTEGER CHECK (performance_rating > 0 AND performance_rating < 6),
    relationship_satisfaction INTEGER CHECK (relationship_satisfaction > 0 AND relationship_satisfaction < 6), 20
    standard_hours INTEGER DEFAULT 80 CHECK (standard_hours > 0),
    stock_option_level INTEGER CHECK (stock_option_level > -1),
    total_working_years INTEGER CHECK (total_working_years > -1),
    training_times_last_year INTEGER CHECK (training_times_last_year > -1),
    work_life_balance INTEGER CHECK (work_life_balance > 0 AND work_life_balance < 6), 25
    years_at_company INTEGER DEFAULT 0 CHECK (years_at_company > -1),
    years_in_current_role INTEGER DEFAULT 0 CHECK (years_in_current_role > -1),
    years_since_last_promotion INTEGER DEFAULT 0 CHECK (years_since_last_promotion > -1),
    years_with_current_manager INTEGER DEFAULT 0 CHECK (years_with_current_manager > -1)
)
"""
#Gets a properly ordered list of values, and checks if it's valid. NOTE: Does not check if primary key is in use for efficiency sake
def check_valid(value_list):
    notNullCatagories = [0, 1, 3, 4, 6, 7, 10, 12, 13, 15]
    for catagory in notNullCatagories: #Not null field is null
        value = value_list[catagory]
        if value == None or value == "": #assume empty entires in csv means Null
            return False
    
    if not re.match(r'^[+-]?[0-9]+$', value_list[1]) or int(value_list[1]) < 18: #Not an adult or non-integer
        return False
    
    if len(value_list[3])>20: #buisness_travel is too long
        return False
    if len(value_list[4])>30: #department is too long
        return False
    if len(value_list[7])>30: #education_field is too long
        return False
    if len(value_list[9])>20: #buisness_travel is too long
        return False
    if len(value_list[13])>30: #job_role is too long
        return False
    if len(value_list[14])>10: #marital_status is too long
        return False
    
    nonNegativeCatagories = [5, 10, 15, 16, 21, 22, 23, 24, 26, 27, 28, 29]
    for catagory in nonNegativeCatagories: #Field that should be a non-negative integer isn't
        value = value_list[catagory]
        if value != None and ((not re.match(r'^[+-]?[0-9]+$', value)) or int(value) < 0): #not Null and not an integer or negative
            return False

    gradingCatagories = [6, 8, 11, 12, 19, 20, 25]
    for catagory in gradingCatagories: #Field for 1-5 integer grading has value outside of that.
        value = value_list[catagory]
        if value != None and (not re.match(r'^[+-]?[0-9]+$', value) or int(value) < 1 or int(value) > 5): #not Null and not an integer or outside 1-5 range
            return False
    
    return True #Everything checks out

#Gets a list of ordered inputs, returns a tuple of a list of valid and non-valid inputs
def check_all_valid(inputs):
    valid = []
    invalid = []
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute("SELECT employee_number FROM employees") #Get the primary keys
                
                primary_keys = set(cur.fetchall()) #get primary keys and turn them into set for efficient look-up. Stored as (int, )
                existing_primary_keys = set()
                for input in inputs:
                    #Not valid if primary keys already in database or valid.
                    if check_valid(input) and (int(input[0]),) not in primary_keys and input[0] not in existing_primary_keys:
                        valid.append(input)
                        existing_primary_keys.add(input[0]) #shouldn't matter it's a string if we keep comparing input[0]
                    else:
                        invalid.append(input)
                return (tuple(valid), tuple(invalid))

            conn.commit() #NOTE: Pretty sure this is unneeded
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

#given a list of values, the desired parameter, and a dictionary of parameters and positions, return the desired parameter
def get_csv_param(value_list, param, catagoryDict):
    if catagoryDict[param] == None:
        return None
    return value_list[catagoryDict[param]]

#Given a value list and a dictionary of parameters and positions, returns an ordered list of parameters
def sort_csv_params(value_list, catagoryDict):
    return [get_csv_param(value_list, "employeenumber", catagoryDict), get_csv_param(value_list, "age", catagoryDict),\
            get_csv_param(value_list, "attrition", catagoryDict), get_csv_param(value_list, "businesstravel", catagoryDict),\
            get_csv_param(value_list, "department", catagoryDict), get_csv_param(value_list, "distancefromhome", catagoryDict), \
            get_csv_param(value_list, "education", catagoryDict), get_csv_param(value_list, "educationfield", catagoryDict),\
            get_csv_param(value_list, "environmentsatisfaction", catagoryDict), get_csv_param(value_list, "gender", catagoryDict),\
            get_csv_param(value_list, "hourlyrate", catagoryDict), get_csv_param(value_list, "jobinvolvement", catagoryDict), \
            get_csv_param(value_list, "joblevel", catagoryDict), get_csv_param(value_list, "jobrole", catagoryDict),\
            get_csv_param(value_list, "maritalstatus", catagoryDict), get_csv_param(value_list, "monthlyrate", catagoryDict),\
            get_csv_param(value_list, "numcompaniesworked", catagoryDict), get_csv_param(value_list, "overtime", catagoryDict), \
            get_csv_param(value_list, "percentsalaryhike", catagoryDict), get_csv_param(value_list, "relationshipsatisfaction", catagoryDict),\
            get_csv_param(value_list, "performancerating", catagoryDict), get_csv_param(value_list, "standardhours", catagoryDict),\
            get_csv_param(value_list, "stockoptionlevel", catagoryDict), get_csv_param(value_list, "totalworkingyears", catagoryDict),\
            get_csv_param(value_list, "trainingtimeslastyear", catagoryDict), get_csv_param(value_list, "worklifebalance", catagoryDict),\
            get_csv_param(value_list, "yearsatcompany", catagoryDict), get_csv_param(value_list, "yearsincurrentrole", catagoryDict),\
            get_csv_param(value_list, "yearssincelastpromotion", catagoryDict), get_csv_param(value_list, "yearswithcurrmanager", catagoryDict)]

#Reads a csv file #UNFINISHED
def read_csv(filename):
    try: #FUTURE: Could probably make things way more efficient with pandas
        with open(filename, mode ='r') as file:
            csvFile = csv.reader(file)
            #Find catagories from CSV file to match up to SQL table
            #Dictionary standardized to help clean data. yearswithcurrmanager is from original data
            catagoryDict = {"employeenumber": None, "age": None, "attrition": None, "businesstravel": None, "department": None, "distancefromhome": None,\
                        "education": None, "educationfield": None, "environmentsatisfaction": None, "gender": None, "hourlyrate": None, "jobinvolvement": None,\
                        "joblevel": None, "jobrole": None, "maritalstatus": None, "monthlyrate": None, "numcompaniesworked": None, "overtime": None,\
                        "percentsalaryhike": None, "performancerating": None, "relationshipsatisfaction": None, "standardhours": None, "stockoptionlevel": None,\
                        "totalworkingyears": None, "trainingtimeslastyear": None, "worklifebalance": None, "yearsatcompany": None, "yearsincurrentrole": None,\
                        "yearssincelastpromotion": None, "yearswithcurrmanager": None}
            catagories = next(csvFile)
            for i in range(len(catagories)):
                catagory = re.sub(r'[^a-zA-Z]', '', catagories[i]).lower()
                if re.sub(r'[^a-zA-Z]', '', catagories[i]).lower() in catagoryDict.keys(): #remove capitalization and non-letters
                    catagoryDict[catagory] = i
                elif catagory == "yearswithcurrentmanager": #In case of CSV file using our SQL scehmatics
                    catagoryDict["yearswithcurrmanager"]=i
            
            notNullCatagories = ["employeenumber", "age", "businesstravel", "department", "education", "educationfield", "hourlyrate", "joblevel", "jobrole", "monthlyrate"]
            for catagory in notNullCatagories:
                if catagoryDict[catagory] == None: #If a Not Null field is Null
                    print(f"Missing catagories in CSV file {filename}.")
                    return
            
            inputs = []
            for line in csvFile:
                sorted = sort_csv_params(line, catagoryDict)
                inputs.append(sorted)
                #print(check_valid(sorted))
            results = check_all_valid(inputs)
            fill_database(results[0]) #Fill database with valid results
            #print("Valid:")
            #for valid in results[0]:
            #    print(valid)
            #print("Invalid:")
            #for invalid in results[1]:
            #    print(invalid)
            print(f"")
    except FileNotFoundError:
        print(f"Error: The file {filename} could not be found.")
    except csv.Error as e:
        print(f"Error: Failed to decode csv from the file {filename}: {e}")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error: The following error occured trying to read csv from {filename}: {e} on line {exc_tb.tb_lineno}")

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

#Drops the employee table. Mostly used for resetting the employee table.
def drop_tables():
    try:
        config = load_config()
        sql = "DROP TABLE employees" #Change when database details decided
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if(table_exists()): #If table exists
                    cur.execute(sql)
                    print("Table Employees dropped")
                else:
                    print("Employees table does not exist")
    except (psycopg2.DatabaseError, Exception) as e:
        print(f"Failed to drop table Employees: {e}")

#Takes a list of commands and performs them, reading any csv or json files given
def read_commands(commands):
    for command in commands:
        if command.endswith(".csv"):
            read_csv(command)
        elif command.endswith(".json"):
            read_json(command)
        elif command == "drop":
            drop_tables()
        else:
            print("Invalid command/file")

if __name__ == '__main__':
    if not table_exists(): #if the employees table doesn't exist, create it
        create_tables()
    if len(sys.argv)>1: #If there are parameters to calling the main function
        read_commands(sys.argv[1:])