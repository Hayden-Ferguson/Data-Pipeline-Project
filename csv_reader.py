import csv
import re
import sys

#File to hold all csv-related functions

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

#Reads a csv file and sorts it's contents. Returns a list of sorted inputs
def read_csv(filename):
    try: #TODO: Could probably make things way more efficient with pandas
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
                if catagory in catagoryDict.keys(): #remove capitalization and non-letters
                    catagoryDict[catagory] = i
                elif catagory == "yearswithcurrentmanager": #In case of CSV file using our SQL scehmatics
                    catagoryDict["yearswithcurrmanager"]=i
            
            notNullCatagories = ["employeenumber", "age", "businesstravel", "department", "education", "educationfield", "hourlyrate", "joblevel", "jobrole", "monthlyrate"]
            for catagory in notNullCatagories:
                if catagoryDict[catagory] == None: #If a Not Null field is Null
                    print(f"Missing non-Null catagories in CSV file {filename}.")
                    return
            
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
        print(f"Error: The following error occured trying to read csv from {filename}: {e} on line {exc_tb.tb_lineno}")