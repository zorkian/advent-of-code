import importlib

from .day import Day

days = {}
for i in range(1, 26):
    try:
        module = importlib.import_module(f".day{i}", package=__package__)
        days[i] = getattr(module, f"Day{i}")
    except (ImportError, AttributeError):
        pass

def get_day(day_number, use_test_data=False) -> Day:
    if day_number in days:
        return days[day_number](use_test_data)
    raise Exception("Unknown day")


__all__ = ["get_day"]
