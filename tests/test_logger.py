import src.logger as logger
import re
import os
from datetime import datetime
import pytest # pyright: ignore[reportMissingImports]

#TODO: Impliment regex to determine if datetime works properly instead of reading around it
#TODO: automatically delete test_logger.txt before starting test to prevent test corruption

def test_log_start():
    logger.log_start('a', 0, 'b', "test_logger.txt")
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0] == "\n"
        assert lines[1][:5] == "-----" #avoiding datetime string
        assert lines[1][-6:] == "-----\n"
        assert lines[2] == "INFO ingest.start source=a rows=0 path=b\n"

    logger.log_start('c', 1, 'd', "test_logger.txt") #testing appending
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0] == "\n"
        assert lines[1][:5] == "-----"
        assert lines[1][-6:] == "-----\n"
        assert lines[2] == "INFO ingest.start source=a rows=0 path=b\n"
        assert lines[3] == "\n"
        assert lines[4][:5] == "-----"
        assert lines[4][-6:] == "-----\n"
        assert lines[5] == "INFO ingest.start source=c rows=1 path=d\n"
    os.remove("test_logger.txt")


def test_log_validation():
    logger.log_validation('a', ([],[1]), "test_logger.txt")
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines == ["INFO ingest.validate source=a valid=0 invalid=1\n"]

    logger.log_validation('b', ([0,1],[1,2,3]), "test_logger.txt") #testing appending
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0] == "INFO ingest.validate source=a valid=0 invalid=1\n"
        assert lines[1] == "INFO ingest.validate source=b valid=2 invalid=3\n"
    os.remove("test_logger.txt")


def test_log_load():
    logger.log_load('a', 0, 1, datetime.now(), "test_logger.txt")
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0][:56] == "INFO ingest.load source=a inserted=0 updated=1 duration="
        assert lines[0][-2:] == "s\n"

    logger.log_load('b', 2, 3, datetime.now(), "test_logger.txt") #testing appending
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0][:56] == "INFO ingest.load source=a inserted=0 updated=1 duration="
        assert lines[0][-2:] == "s\n"
        assert lines[1][:56] == "INFO ingest.load source=b inserted=2 updated=3 duration="
        assert lines[1][-2:] == "s\n"
    os.remove("test_logger.txt")

def test_log_end():
    logger.log_end('a', "success", "test_logger.txt")
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines == ["INFO ingest.end source=a status=success\n"]

    logger.log_end('b', "failure", "test_logger.txt") #testing appending
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0] == "INFO ingest.end source=a status=success\n"
        assert lines[1] == "INFO ingest.end source=b status=failure\n"
    os.remove("test_logger.txt")


def test_log_rejects():
    rejects = [('a', 'b')]
    logger.log_rejects(rejects, "test_logger.txt")
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0] == "\n"
        assert lines[1][:5] == "-----" #avoiding datetime string
        assert lines[1][-6:] == "-----\n"
        assert lines[2] == "a\n"
        assert lines[3] == "reason: b\n"

    rejects = [('c', 'd'), ('e', 'f')]
    logger.log_rejects(rejects, "test_logger.txt") #testing appending
    with open("test_logger.txt", "r") as log:
        lines = log.readlines()
        assert lines[0] == "\n"
        assert lines[1][:5] == "-----" 
        assert lines[1][-6:] == "-----\n"
        assert lines[2] == "a\n"
        assert lines[3] == "reason: b\n"
        assert lines[4] == "\n"
        assert lines[5][:5] == "-----" 
        assert lines[5][-6:] == "-----\n"
        assert lines[6] == "c\n"
        assert lines[7] == "reason: d\n"
        assert lines[8] == "e\n"
        assert lines[9] == "reason: f\n"
    os.remove("test_logger.txt")