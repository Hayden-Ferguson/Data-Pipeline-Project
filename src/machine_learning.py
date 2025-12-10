import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

catagoryList=["employee_number", "age", "attrition", "business_travel", "department", "distance_from_home", \
    "education", "education_field", "environment_satisfaction", "gender", "hourly_rate", "job_involvement", "job_level", \
    "job_role", "marital_status", "monthly_rate", "num_companies_worked", "overtime", "percent_salary_hike", "performance_rating", \
    "relationship_satisfaction", "standard_hours", "stock_option_level", "total_working_years", "training_times_last_year", \
    "work_life_balance", "years_at_company", "years_in_current_role", "years_since_last_promotion", "years_with_current_manager"]

#splits data into testing and training data, and removes data not being trained on
def split_data(data): #TODO: make this random, probably with sklearn.model_selection.train_test_split
    unsplit = data.drop(columns=["employee_number"])
    middle = len(data)//2
    training = unsplit.iloc[:middle].reset_index(drop=True)
    testing = unsplit.iloc[middle:].reset_index(drop=True)
    return (training, testing)

#Given training data, train a Logistic Regression model with it and return the model
def train(train):
    X = train.drop("attrition", axis=1)
    y = train["attrition"]

    X = pd.get_dummies(X, drop_first=True)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = LogisticRegression(max_iter=500)
    model.fit(X_scaled, y)

    return model

#Given a model and test
def test(model, test):
    X = test.drop("attrition", axis=1)
    y = test["attrition"]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    y_pred = model.predict(X_scaled)

    report = classification_report(y, y_pred)
    print(report)
    return report