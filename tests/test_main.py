import main
import src.sql_interface as sql_interface
import os
import json
from sklearn.linear_model import LogisticRegression
import pytest # pyright: ignore[reportMissingImports]

def test_filter_inputs():
    unfiltered = [[0, "a", (), 'd'], [1, "", [], None]]
    filtered = main.filter_inputs(unfiltered)
    assert filtered == [[0, "a", (), 'd'], [1, None, [], None]]


def test_check_valid():

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (True, "Duplicate primary key") #valid

    input = ("20", "29", "False", 'Travel_Rarely', 'Research & Development', "21", "4", 'Life Sciences', "2", 'Female', "51", "4", "3", 'Manufacturing Director', \
             'Divorced', "10195", "1", "False", "11", "3", "3", "80", "1", "10", "1", "3", "10", "9", "8", "8")
    assert main.check_valid(input) == (True, "Duplicate primary key") #valid

    input = (20, 29, None, 'Travel_Rarely', 'Research & Development', None, 4, 'Life Sciences', None, None, 51, None, 3, 'Manufacturing Director', \
             None, 10195, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    assert main.check_valid(input) == (True, "Duplicate primary key") #valid

    input = (None, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "employee_number is Null")

    input = (20, None, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "age is Null")

    input = (20, 29, False, None, 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "business_travel is Null")

    input = (20, 29, False, 'Travel_Rarely', None, 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "department is Null")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, None, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "education is Null")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, None, 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "education_field is Null")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', None, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "hourly_rate is Null")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, None, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "job_level is Null")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, None, \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "job_role is Null")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', None, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "monthly_rate is Null")

    input = (20, 17, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "age is 17, which is below 18 or not an integer")

    input = (20, "twenty-nine", False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "age is twenty-nine, which is below 18 or not an integer")

    input = (20, 29, False, 'aaaaaaaaaaaaaaaaaaaaa', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "buisness_travel is aaaaaaaaaaaaaaaaaaaaa, which is too long")

    input = (20, 29, False, 'Travel_Rarely', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "department is aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, which is too long")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "education_field is aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, which is too long")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'aaaaaaaaaaaaaaaaaaaaa', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "gender is aaaaaaaaaaaaaaaaaaaaa, which is too long")
    
    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "job_role is aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa, which is too long")
    
    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'aaaaaaaaaaa', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "marital_status is aaaaaaaaaaa, which is too long")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', -1, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "distance_from_home is -1, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', "twenty", 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "distance_from_home is twenty, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', -1, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "hourly_rate is -1, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', -1, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "monthly_rate is -1, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, -1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "num_companies_worked is -1, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, -1, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "standard_hours is -1, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, -1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "stock_option_level is -1, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, -10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "total_working_years is -10, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, -1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "training_times_last_year is -1, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, -10, 9, 8, 8)
    assert main.check_valid(input) == (False, "years_at_company is -10, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, -9, 8, 8)
    assert main.check_valid(input) == (False, "years_in_current_role is -9, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, -8, 8)
    assert main.check_valid(input) == (False, "years_since_last_promotion is -8, which is either negative or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, -8)
    assert main.check_valid(input) == (False, "years_with_current_manager is -8, which is either negative or not an integer")
    
    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 0, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "education is 0, which is outside of the 1-5 range or not an integer")
    
    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 6, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "education is 6, which is outside of the 1-5 range or not an integer")
    
    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, "one", 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "education is one, which is outside of the 1-5 range or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 0, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "environment_satisfaction is 0, which is outside of the 1-5 range or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 0, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "job_involvement is 0, which is outside of the 1-5 range or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 0, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "job_level is 0, which is outside of the 1-5 range or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 0, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "performance_rating is 0, which is outside of the 1-5 range or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 0, 80, 1, 10, 1, 3, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "relationship_satisfaction is 0, which is outside of the 1-5 range or not an integer")

    input = (20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 0, 10, 9, 8, 8)
    assert main.check_valid(input) == (False, "work_life_balance is 0, which is outside of the 1-5 range or not an integer")

    
def test_check_all_valid():
    inputs = []
    inputs.append((20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8))
    inputs.append((20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8))
    inputs.append((None, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8))
    results = main.check_all_valid(inputs)
    assert results[0] == ((20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8),)
    assert results[1][0] == ((20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8), "Duplicate primary key")
    assert results[1][1] == ((None, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8), "employee_number is Null")
    
def test_upsert_call(): #uses sql_interface functions for simplicity #TODO: check last lines of log
    if sql_interface.table_exists("test"):
        sql_interface.drop_table("test")
    sql_interface.create_tables("test")
    inputs = []
    inputs.append((20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8))
    inputs.append((20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8))
    inputs.append((21, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8))
    main.upsert_call(inputs, "s", "test")
    
    assert sql_interface.count_rows("test") == 2
    inputs = []
    inputs.append((20, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8)) #testing updates
    inputs.append((22, 29, False, 'Travel_Rarely', 'Research & Development', 21, 4, 'Life Sciences', 2, 'Female', 51, 4, 3, 'Manufacturing Director', \
             'Divorced', 10195, 1, False, 11, 3, 3, 80, 1, 10, 1, 3, 10, 9, 8, 8))
    main.upsert_call(inputs, "s", "test")
    assert sql_interface.count_rows("test") == 3
    sql_interface.drop_table("test")

def test_read_commands():
    if sql_interface.table_exists("test"):
        sql_interface.drop_table("test")
    sql_interface.create_tables("test")
    
    with open("data/test.csv", "w") as file:
        file.write("Age,Attrition,BusinessTravel,DailyRate,Department,DistanceFromHome,Education,EducationField,EmployeeCount,\
        EmployeeNumber,EnvironmentSatisfaction,Gender,HourlyRate,JobInvolvement,JobLevel,JobRole,JobSatisfaction,MaritalStatus,\
        MonthlyIncome,MonthlyRate,NumCompaniesWorked,Over18,OverTime,PercentSalaryHike,PerformanceRating,RelationshipSatisfaction,\
        StandardHours,StockOptionLevel,TotalWorkingYears,TrainingTimesLastYear,WorkLifeBalance,YearsAtCompany,YearsInCurrentRole,\
        YearsSinceLastPromotion,YearsWithCurrManager\n")
        file.write("41,Yes,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,1,2,Female,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5\n")
        file.write("41,No,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,5,2,Male,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5\n")
        file.write("41,No,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,7,2,Male,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5\n")
        file.write("41,No,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,2,2,Male,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5\n")
        file.write("41,Yes,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,3,2,Male,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5\n")
        file.write("41,Yes,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,4,2,Female,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5")
    main.read_commands(["data/test.csv"], "test")
    assert sql_interface.count_rows("test") == 6
    main.read_commands(["read"], "test")
    with open("sql_reader.txt", "r") as output:
        assert output.readlines()[0] == "(1, 41, True, 'Travel_Rarely', 'Sales', 1, 2, 'Life Sciences', 2, 'Female', 94, 3, 2, 'Sales Executive',"\
                                      " 'Single', 19479, 8, True, 11, 3, 1, 80, 0, 8, 0, 1, 6, 4, 0, 5)\n"
    model, report = main.read_commands(["train"], "test")
    assert isinstance(model, LogisticRegression)
    assert isinstance(report, str)
    assert "precision" in report
    assert "recall" in report
    assert "f1-score" in report
    main.read_commands(["clear"], "test")
    assert sql_interface.count_rows("test") == 0
    #TODO: Make json command
    dictionary = [{"Age": 41, "Attrition": "Yes", "BusinessTravel": "Travel_Rarely", "DailyRate": 1102, "Department": "Sales",\
    "DistanceFromHome": 1, "Education": 2, "EducationField": "Life Sciences", "EmployeeCount": 1, "EmployeeNumber": 1,\
    "EnvironmentSatisfaction": 2, "Gender": "Female", "HourlyRate": 94, "JobInvolvement": 3, "JobLevel": 2, "JobRole": "Sales Executive",\
    "JobSatisfaction": 4, "MaritalStatus": "Single", "MonthlyIncome": 5993, "MonthlyRate": 19479, "NumCompaniesWorked": 8, "Over18": "Y",\
    "OverTime": "Yes", "PercentSalaryHike": 11, "PerformanceRating": 3, "RelationshipSatisfaction": 1, "StandardHours": 80,\
    "StockOptionLevel": 0, "TotalWorkingYears": 8, "TrainingTimesLastYear": 0, "WorkLifeBalance": 1, "YearsAtCompany": 6,\
    "YearsInCurrentRole": 4, "YearsSinceLastPromotion": 0, "YearsWithCurrManager": 5}]
    with open("data/test.json", "w") as file:
        json.dump(dictionary, file, indent=4)
    main.read_commands(["data/test.json"], "test")
    assert sql_interface.count_rows("test") == 1
    main.read_commands(["drop"], "test")
    assert sql_interface.table_exists("test") == False
    os.remove("data/test.csv")
    os.remove("data/test.json")