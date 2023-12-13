import sys
sys.path.append(".")

import pytest
from unittest.mock import MagicMock
from src.scheduler import *


def test_char_flip():
    print(char_flip("0123456789", 2000, 10, 3))   

def test_char_del():
    print(char_del("0123456789", 3, 2))

def test_char_ins():
    print(char_ins("123456789", 2, 7))

def test_havoc():
    print(Havoc("123456789"))

def test_splice():
    print(1, Splice("12345789", "abcdefg"))
    print(2, Splice("12345", "abc"))
    print(3, Splice("123", "abcd"))
    print(4, Splice("1", "a"))
    print(5, Splice("1", ""))
    print(6, Splice("", "1"))
    print(7, Splice("", ""))

def test_schedule():
    print(schedule(["0123456789"], 10))

if __name__ == "__main__":
    # test_char_del()
    # test_schedule()
    test_havoc()