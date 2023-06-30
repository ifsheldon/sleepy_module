import time

from src.sleepy_module import SleepyModule
import torch


class Data(torch.nn.Module):

    def __init__(self):
        super().__init__()
        self.data = torch.nn.Parameter(torch.ones(1))


def test_sleepy_module_simple():
    cuda = torch.device("cuda:0")
    data = Data().to(cuda)
    sleepy = SleepyModule(cuda, data, 1, rest_device="cpu", time_immediately=True)
    time.sleep(2.)
    assert sleepy.mod.data.device == torch.device("cpu")
