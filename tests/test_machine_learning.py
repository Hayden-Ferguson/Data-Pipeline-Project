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

def test_train():
    data = pd.DataFrame([{"attrition":"Yes", "a":1}, {"attrition":"Yes", "a":2}, {"attrition":"No", "a":3}, {"attrition":"No", "a":4}])
    model = machine_learning.train(data)
    assert isinstance(model, LogisticRegression)