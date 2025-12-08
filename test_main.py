import main
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