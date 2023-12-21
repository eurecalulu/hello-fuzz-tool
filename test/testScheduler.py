import sys
sys.path.append(".")

from src.scheduler import *

def test_schedule():
    print(schedule(["0123456789"], [1], 1000))

if __name__ == "__main__":
    test_schedule()
    # test_char_del()
    # test_char_flip()
    # test_case_conversion()
    # test_repeat_pattern()
    # test_boundary_change()