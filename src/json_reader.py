import json
import sys
import re
import os

#List of catagories for reference #TODO: modify functions to not use regex if not required
#NOTE: years_with_current_manager was YearsWithCurrManager in original source
standard_catagories=["employee_number", "age", "attrition", "business_travel", "department", "distance_from_home", \
    "education", "education_field", "environment_satisfaction", "gender", "hourly_rate", "job_involvement", "job_level", \
    "job_role", "marital_status", "monthly_rate", "num_companies_worked", "overtime", "percent_salary_hike", "performance_rating", \
    "relationship_satisfaction", "standard_hours", "stock_option_level", "total_working_years", "training_times_last_year", \
    "work_life_balance", "years_at_company", "years_in_current_role", "years_since_last_promotion", "years_with_current_manager"]

#converts dictionaries from json to ordered list given a list of dictionaries and ordered list of desired catagories
def convert_json(dictionaries, catagory_list=standard_catagories):
    results = []
    for dictionary in dictionaries:
        result = []
        for catagory in catagory_list:
            if catagory != "years_with_current_manager":
                standardized_catagory = re.sub(r'[^a-zA-Z]', '', catagory) #to account for differences in format
                for k, v in dictionary.items(): #required due to different catagory name variations
                    if re.sub(r'[^a-zA-Z]', '', k).lower() == standardized_catagory:
                        result.append(v)
                        break
            else: #if years_with_current_manager, which has different name in original source
                for k, v in dictionary.items(): #required due to different catagory name variations
                    standard_key = re.sub(r'[^a-zA-Z]', '', k).lower()
                    if standard_key == "yearswithcurrmanager" or standard_key == "yearswithcurrentmanager":
                        result.append(v)
                        break
        results.append(result)
    return results

#Reads and prints a JSON file
def read_json(filename, catagory_list=standard_catagories):
    try:
        with open(filename, mode ='r') as file:
            #df = pd.read_json(filename)
            #print(df.head(1).to_dict())
            data = json.load(file) #load and loads are for file vs string
            #dictonaries = json.dumps(data) #same for dump and dumps output
            converted = convert_json(data, catagory_list) #Convert dictionaries to ordered lists
            return converted

    except FileNotFoundError:
        print(f"Error: The file {filename} could not be found.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from the file {filename}: {e}")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"Error: The following error occured trying to read JSON from {filename}: {e} on line {exc_tb.tb_lineno} in {file_name}")