import csv_reader
import pytest

def test_get_catagory_dict():
    desired_catagories = ["One", "2Two", "Th_ree"] #test basic functionality
    csv_catagories = ["thRee", "one_", "two"]
    catagoryDict = csv_reader.get_catagory_dict(desired_catagories, csv_catagories)
    assert catagoryDict["one"] == 1
    assert catagoryDict["two"] == 2
    assert catagoryDict["three"] == 0

    desired_catagories = ["years_with_current_manager"] #tests hardcoded exception
    csv_catagories = ["YearsWithCurrManager"]
    catagoryDict = csv_reader.get_catagory_dict(desired_catagories, csv_catagories)
    assert catagoryDict["yearswithcurrentmanager"] == 0
