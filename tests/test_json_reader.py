import src.json_reader as json_reader
import os
import pytest # pyright: ignore[reportMissingImports]

def test_convert_json():
    dictonaries = [{"A":"b", "Years_With_Curr_Manager":3}, {"yearswithcurrentmanager":4, "a":"C"}]
    results = json_reader.convert_json(dictonaries, ["a", "years_with_current_manager"])
    assert results[0] == ["b", 3]
    assert results[1] == ["C", 4]
