from typing import Any, Callable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_STOPPED


class Sleepy:

    def __init__(self,
                 data: Any,
                 interval: int,
                 to_rest_func: Callable,
                 time_immediately: bool = True):
        self.data = data
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(func=lambda: to_rest_func(self.data), trigger="interval", seconds=interval)
        if time_immediately:
            self.scheduler.start()

    def start_timing(self):
        if self.scheduler.state == STATE_STOPPED:
            self.scheduler.start()
