import csv_reader
import pytest # pyright: ignore[reportMissingImports]

def test_get_catagory_dict():
    desired_catagories = ["One", "2Two", "Th_ree"] #test basic functionality
    csv_catagories = ["thRee", "one_", "two"]
    catagoryDict = csv_reader.get_catagory_dict(desired_catagories, csv_catagories)
    assert catagoryDict["one"] == 1
    assert catagoryDict["two"] == 2
    assert catagoryDict["three"] == 0

    desired_catagories = ["One", "2Two", "Th_ree"] #test correct order
    csv_catagories = ["one_", "two", "thRee"]
    catagoryDict = csv_reader.get_catagory_dict(desired_catagories, csv_catagories)
    assert catagoryDict["one"] == 0
    assert catagoryDict["two"] == 1
    assert catagoryDict["three"] == 2

    desired_catagories = ["one", "two", "three"] #test exact matches
    csv_catagories = ["one", "two", "three"]
    catagoryDict = csv_reader.get_catagory_dict(desired_catagories, csv_catagories)
    assert catagoryDict["one"] == 0
    assert catagoryDict["two"] == 1
    assert catagoryDict["three"] == 2

    desired_catagories = ["years_with_current_manager"] #tests hardcoded exception
    csv_catagories = ["YearsWithCurrManager"]
    catagoryDict = csv_reader.get_catagory_dict(desired_catagories, csv_catagories)
    assert catagoryDict["yearswithcurrentmanager"] == 0

def test_get_csv_param():
    value_list = [1,2,3]
    catagoryDict = {'a': 0, 'b': 1, 'c':2, 'd':None}
    assert csv_reader.get_csv_param(value_list, 'a', catagoryDict) == 1
    assert csv_reader.get_csv_param(value_list, 'b', catagoryDict) == 2
    assert csv_reader.get_csv_param(value_list, 'c', catagoryDict) == 3
    assert csv_reader.get_csv_param(value_list, 'd', catagoryDict) == None
    assert csv_reader.get_csv_param(value_list, 'e', catagoryDict) == None

def test_sort_csv_params():
    value_list = [1,2,3,4]
    catagoryDict = {'a': 0, 'b': 1, 'c':2, 'd':3}
    catagoryList = ['b', 'c', 'a']
    assert csv_reader.sort_csv_params(value_list, catagoryList, catagoryDict) == [2,3,1]

    #Checks if None is handled
    value_list = [1,None,3]
    catagoryDict = {'a': 0, 'b': 1, 'c':2, 'd':None}
    catagoryList = ['b', 'c', 'a']
    assert csv_reader.sort_csv_params(value_list, catagoryList, catagoryDict) == [None,3,1]

def test_read_csv():
    with open("data/test.csv", "w") as file:
        file.write("Age,Attrition,BusinessTravel,DailyRate,Department,DistanceFromHome,Education,EducationField,EmployeeCount,\
        EmployeeNumber,EnvironmentSatisfaction,Gender,HourlyRate,JobInvolvement,JobLevel,JobRole,JobSatisfaction,MaritalStatus,\
        MonthlyIncome,MonthlyRate,NumCompaniesWorked,Over18,OverTime,PercentSalaryHike,PerformanceRating,RelationshipSatisfaction,\
        StandardHours,StockOptionLevel,TotalWorkingYears,TrainingTimesLastYear,WorkLifeBalance,YearsAtCompany,YearsInCurrentRole,\
        YearsSinceLastPromotion,YearsWithCurrManager\n")
        file.write("41,Yes,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,1,2,Female,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5")
    results = csv_reader.read_csv("data/test.csv")
    assert results == [['1','41','Yes','Travel_Rarely','Sales','1','2','Life Sciences','2','Female','94','3','2','Sales Executive','Single',\
                        '19479','8','Yes','11','3','1','80','0','8','0','1','6','4','0','5']]
    
    with open("data/test.csv", "w") as file: #Test missing non-null catagory
        file.write("Attrition,BusinessTravel,DailyRate,Department,DistanceFromHome,Education,EducationField,EmployeeCount,\
        EmployeeNumber,EnvironmentSatisfaction,Gender,HourlyRate,JobInvolvement,JobLevel,JobRole,JobSatisfaction,MaritalStatus,\
        MonthlyIncome,MonthlyRate,NumCompaniesWorked,Over18,OverTime,PercentSalaryHike,PerformanceRating,RelationshipSatisfaction,\
        StandardHours,StockOptionLevel,TotalWorkingYears,TrainingTimesLastYear,WorkLifeBalance,YearsAtCompany,YearsInCurrentRole,\
        YearsSinceLastPromotion,YearsWithCurrManager\n")
        file.write(",Yes,Travel_Rarely,1102,Sales,1,2,Life Sciences,1,1,2,Female,94,3,2,Sales Executive,4,Single,5993,19479,8,Y,Yes,11,3,1,80,0,8,0,1,6,4,0,5")
    assert csv_reader.read_csv("data/test.csv") is None