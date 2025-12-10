import src.machine_learning as machine_learning
import pandas as pd
import pytest # pyright: ignore[reportMissingImports]

def test_split_data():
    data = pd.DataFrame([{"employee_number":1, "a":"b"}, {"employee_number":2, "a":"c"}])
    training, testing = machine_learning.split_data(data)
    dataframe = pd.DataFrame({"a":["b"]})
    assert training.equals(dataframe)
    dataframe = pd.DataFrame({"a":["c"]})
    assert testing.equals(dataframe)