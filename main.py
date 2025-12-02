import sys
import re
import os
#import pandas as pd
from datetime import datetime

import csv_reader
import json_reader
import sql_interface
import logger

#NOTE: robust inputs, can recognize caragory names despite differences with capitalization or underscores.
#TODO: incorporate machine learning to predict quitting
#TODO: find ways people want to use this data

#List of catagories for reference #TODO: modify functions to not use regex if not required
#NOTE: years_with_current_manager was YearsWithCurrManager in original source
catagoryList=["employee_number", "age", "attrition", "business_travel", "department", "distance_from_home", \
    "education", "education_field", "environment_satisfaction", "gender", "hourly_rate", "job_involvement", "job_level", \
    "job_role", "marital_status", "monthly_rate", "num_companies_worked", "overtime", "percent_salary_hike", "performance_rating", \
    "relationship_satisfaction", "standard_hours", "stock_option_level", "total_working_years", "training_times_last_year", \
    "work_life_balance", "years_at_company", "years_in_current_role", "years_since_last_promotion", "years_with_current_manager"]

#Given a tuple of inputs, replace empty string with None. TODO: Would set to DEFAULT with sql.SQL("DEFAULT"), but interferes with other functions.
def filter_inputs(input_list):
    params = len(input_list[0])
    filtered = input_list.copy() #Avoid modifying the original
    for i in range(len(input_list)):
        for j in range(params):
            if input_list[i][j] == "": #If a parameter is an empty string
                filtered[i][j] = None #Set it to none
    return filtered

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
    try:
        notNullCatagories = [0, 1, 3, 4, 6, 7, 10, 12, 13, 15]
        for catagory in notNullCatagories: #Not null field is null
            value = value_list[catagory]
            if value == None or value == "": #assume empty entires in csv means Null
                return (False, f"{catagoryList[catagory]} is Null")
        
        #print(type(value))
        if not (type(value_list[1]) == int or re.match(r'^[+-]?[0-9]+$', value_list[1])) or int(value_list[1]) < 18: #Not an adult or non-integer
            return (False, f"age is {value_list[1]}, which is below 18 or not an integer")
        
        if len(value_list[3])>20: #buisness_travel is too long
            return (False, f"buisness_travel is {value_list[3]}, which is too long")
        if len(value_list[4])>30: #department is too long
            return (False, f"department is {value_list[4]}, which is too long")
        if len(value_list[7])>30: #education_field is too long
            return (False, f"education_field is {value_list[7]}, which is too long")
        if len(value_list[9])>20: #gender is too long
            return (False, f"gender is {value_list[9]}, which is too long")
        if len(value_list[13])>30: #job_role is too long
            return (False, f"job_role is {value_list[13]}, which is too long")
        if len(value_list[14])>10: #marital_status is too long
            return (False, f"marital_status is {value_list[14]}, which is too long")
        
        nonNegativeCatagories = [5, 10, 15, 16, 21, 22, 23, 24, 26, 27, 28, 29]
        for catagory in nonNegativeCatagories: #Field that should be a non-negative integer isn't
            value = value_list[catagory]
            if value != None and (not (type(value) == int or re.match(r'^[+-]?[0-9]+$', value)) or int(value) < 0): #not Null and not an integer or negative
                return (False, f"{catagoryList[catagory]} is {value}, which is either negative or not an integer")

        gradingCatagories = [6, 8, 11, 12, 19, 20, 25]
        for catagory in gradingCatagories: #Field for 1-5 integer grading has value outside of that.
            value = value_list[catagory] #not Null and not an integer or outside 1-5 range
            if value != None and (not (type(value) == int or re.match(r'^[+-]?[0-9]+$', value)) or int(value) < 1 or int(value) > 5): 
                return (False, f"{catagoryList[catagory]} is {value}, which is outside of the 1-5 range or not an integer")
        
        return (True, "Duplicate primary key") #Everything checks out, if rejected it's due to being a duplicate
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(f"Error: The following error occured trying to validate values: {e} on line {exc_tb.tb_lineno}")

#Gets a list of ordered inputs, returns a tuple of a list of valid and non-valid inputs. Does not allow duplicate keys in same insert.
def check_all_valid(inputs):
    valid = []
    invalid = []
    existing_primary_keys = set()
    for input in inputs:
        #Not valid if primary keys already in database or valid.
        validity = check_valid(input)
        if validity[0] and input[0] not in existing_primary_keys:
            valid.append(input)
            existing_primary_keys.add(input[0]) #shouldn't matter it's a string if we keep comparing input[0]
        else:
            invalid.append((input, validity[1]))
    return (tuple(valid), tuple(invalid))

#Does all the stuff that needs to be done when upsert is called, given sorted inputs and filename
def upsert_call(inputs, filename):
    try:
        logger.log_start(filename, len(inputs), filename)
        filtered = filter_inputs(inputs)
        validated = check_all_valid(filtered)
        logger.log_validation(filename, validated)
        logger.log_rejects(validated[1])
        start = datetime.now()
        results = sql_interface.fill_database(validated[0]) #Fill database with valid results
        logger.log_load(filename, results[0], results[1], start)
        logger.log_end(filename)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"Error: The following error occured trying to upsert from {filename}: {e} on line {exc_tb.tb_lineno} in {file_name}")

#Takes a list of commands and performs them, reading any csv or json files given
def read_commands(commands):
    for command in commands:
        if command.endswith(".csv"):
            inputs = csv_reader.read_csv(command)
            if inputs is not None:
                upsert_call(inputs, command)
        elif command.endswith(".json"):
            inputs = json_reader.read_json(command)
            upsert_call(inputs, command)
        elif command.lower() == "drop":
            sql_interface.drop_table()
            with open("logger.txt", "a") as log: #log dropping table
                log.write(f"\nemployees table dropped at {datetime.now()}\n")
        elif command.lower() == "read":
            sql_interface.read_table()
        elif command.lower() == "clear" or command.lower() == "truncate":
            sql_interface.clear_table()
            with open("logger.txt", "a") as log: #log truncating table
                log.write(f"\nemployees table truncated at {datetime.now()}\n")
        else:
            print("Invalid command/file")

if __name__ == '__main__':
    if not sql_interface.table_exists(): #if the employees table doesn't exist, create it
        sql_interface.create_tables()
        with open("logger.txt", "a") as log: #log table creation
            log.write(f"\nemployees table created at {datetime.now()}\n")
    if len(sys.argv)>1: #If there are parameters to calling the main function
        read_commands(sys.argv[1:])