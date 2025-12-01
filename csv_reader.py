import csv
import re
import sys
import os

#File to hold all csv-related functions

#List of catagories for reference
#NOTE: years_with_current_manager was YearsWithCurrManager in original source
catagoryList=["employee_number", "age", "attrition", "business_travel", "department", "distance_from_home", \
    "education", "education_field", "environment_satisfaction", "gender", "hourly_rate", "job_involvement", "job_level", \
    "job_role", "marital_status", "monthly_rate", "num_companies_worked", "overtime", "percent_salary_hike", "performance_rating", \
    "relationship_satisfaction", "standard_hours", "stock_option_level", "total_working_years", "training_times_last_year", \
    "work_life_balance", "years_at_company", "years_in_current_role", "years_since_last_promotion", "years_with_current_manager"]

#returns a dictionary of catagories to csv placement given list of desired catagory order and list of actual catagories
def get_catagory_dict(desired_catagories, csv_catagories):
    catagoryDict = {}
    for catagory in desired_catagories:
        catagoryDict[re.sub(r'[^a-zA-Z]', '', catagory).lower()] = None #remove capitalization and non-letters & set default value
    for i in range(len(csv_catagories)):
        catagory = re.sub(r'[^a-zA-Z]', '', csv_catagories[i]).lower() #remove capitalization and non-letters
        if catagory in catagoryDict.keys(): 
            catagoryDict[catagory] = i
        elif catagory == "yearswithcurrmanager": #In case of CSV file using old SQL scehmatics (default)
            catagoryDict["yearswithcurrentmanager"]=i
    return catagoryDict

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
            get_csv_param(value_list, "yearssincelastpromotion", catagoryDict), get_csv_param(value_list, "yearswithcurrentmanager", catagoryDict)]

#Reads a csv file and sorts it's contents. Returns a list of sorted inputs
def read_csv(filename):
    try: #TODO: Could probably make things way more efficient with pandas
        with open(filename, mode ='r') as file:
            csvFile = csv.reader(file)
            #Find catagories from CSV file to match up to SQL table
            #Dictionary standardized to help clean data. yearswithcurrmanager is from original data
            catagories = next(csvFile) #reads catagories of csv
            catagoryDict = get_catagory_dict(catagoryList, catagories) #gets dictionary of catagories and their position in list
            notNullCatagories = ["employeenumber", "age", "businesstravel", "department", "education", "educationfield", "hourlyrate", "joblevel", "jobrole", "monthlyrate"]
            for catagory in notNullCatagories: #ensures all non-null field exist
                if catagoryDict[catagory] == None: #If a Not Null field is Null
                    print(f"Missing non-Null catagories in CSV file {filename}.")
                    return None
            
            inputs = [] #NOTE: lines with " causes errors
            for line in csvFile: #Function does not do multiple lines at once do to limits of reading file
                sorted = sort_csv_params(line, catagoryDict) 
                inputs.append(sorted)
            return inputs
        
    except FileNotFoundError:
        print(f"Error: The file {filename} could not be found.")
    except csv.Error as e:
        print(f"Error: Failed to decode csv from the file {filename}: {e}")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"Error: The following error occured trying to read csv from {filename}: {e} on line {exc_tb.tb_lineno} in {file_name}")