import pandas as pd
import sklearn

catagoryList=["employee_number", "age", "attrition", "business_travel", "department", "distance_from_home", \
    "education", "education_field", "environment_satisfaction", "gender", "hourly_rate", "job_involvement", "job_level", \
    "job_role", "marital_status", "monthly_rate", "num_companies_worked", "overtime", "percent_salary_hike", "performance_rating", \
    "relationship_satisfaction", "standard_hours", "stock_option_level", "total_working_years", "training_times_last_year", \
    "work_life_balance", "years_at_company", "years_in_current_role", "years_since_last_promotion", "years_with_current_manager"]

#splits data into testing and training data, and removes data not being trained on
def split_data(data):
    unsplit = data.drop(columns=["employee_number"])
    middle = len(data)//2
    training = unsplit.iloc[:middle].reset_index(drop=True)
    testing = unsplit.iloc[middle:].reset_index(drop=True)
    return (training, testing)