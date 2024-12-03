from .day import Day
from .day1 import Day1
from .day2 import Day2
from .day3 import Day3


def get_day(day_number, use_test_data=False) -> Day:
    if day_number == 1:
        return Day1(use_test_data)
    elif day_number == 2:
        return Day2(use_test_data)
    elif day_number == 3:
        return Day3(use_test_data)
    raise Exception("Unknown day")


__all__ = ["get_day"]
