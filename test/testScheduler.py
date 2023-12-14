import sys
sys.path.append(".")

from src.scheduler import *


def test_char_flip():
    print(char_flip("0123456789", 1, 10, 3))   

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

def test_char_change():
    print(char_change("123456789", 1))
    print(char_change("123456789", 2))

def test_bit_revert():
    print(bit_revert("12345", 5))

def test_case_conversion():
    print(case_conversion("aBcde", 0))
    print(case_conversion("aBcde", 1))
    print(case_conversion("aBcde", 2))

def test_repeat_pattern():
    print(repeat_pattern("123456789", 1, 9))
    print(repeat_pattern("123456789", 2, 9))
    print(repeat_pattern("123456789", 2, 8))

def test_boundary_change():
    print(boundary_change("123456789", 0))
    print(boundary_change("123456789", 1))
    print(boundary_change("123456789", 2))


def test_schedule():
    print(schedule(["0123456789"], 1000))

if __name__ == "__main__":
    test_schedule()
    # test_char_del()
    # test_char_flip()
    # test_case_conversion()
    # test_repeat_pattern()
    # test_boundary_change()