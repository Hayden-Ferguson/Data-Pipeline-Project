import src.machine_learning as machine_learning
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pytest # pyright: ignore[reportMissingImports]

def test_split_data():
    data = pd.DataFrame([{"employee_number":1, "a":"b"}, {"employee_number":2, "a":"c"}])
    training, testing = machine_learning.split_data(data)
    dataframe = pd.DataFrame({"a":["b"]})
    assert training.equals(dataframe)
    dataframe = pd.DataFrame({"a":["c"]})
    assert testing.equals(dataframe)

#Prove a model is created
def test_train():
    data = pd.DataFrame([{"attrition":"Yes", "a":1}, {"attrition":"Yes", "a":2}, {"attrition":"No", "a":3}, {"attrition":"No", "a":4}])
    model = machine_learning.train(data)
    assert isinstance(model, LogisticRegression)

#Prove a report is made
def test_test():
    data = pd.DataFrame([{"attrition":"Yes", "a":1}, {"attrition":"Yes", "a":2}, {"attrition":"No", "a":3}, {"attrition":"No", "a":4}])
    model = machine_learning.train(data)
    report = machine_learning.test(model, data)
    assert isinstance(report, str)
    assert "precision" in report
    assert "recall" in report
    assert "f1-score" in report

#Proof train_and_test() returns values from train() and test()
def test_train_and_test():
    data = pd.DataFrame([{"employee_number":1, "attrition":"Yes", "a":1}, {"employee_number":3, "attrition":"No", "a":2},\
                          {"employee_number":6, "attrition":"No", "a":3}, {"employee_number":7, "attrition":"Yes", "a":4}])
    model, report = machine_learning.train_and_test(data)
    assert isinstance(model, LogisticRegression)
    assert isinstance(report, str)
    assert "precision" in report
    assert "recall" in report
    assert "f1-score" in report
