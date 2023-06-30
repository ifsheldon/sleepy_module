import time

from src.sleepy_module import Sleepy


class Data:
    def __init__(self, data: str):
        self.data = data


def test_sleepy():
    data = Data("hey")

    def func(x):
        x.data = "yo"

    sleepy = Sleepy(data, 1, func, time_immediately=True)
    time.sleep(2.0)
    assert sleepy.data.data == "yo"
