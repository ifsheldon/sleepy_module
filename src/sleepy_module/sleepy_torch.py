from datetime import datetime, timedelta
from typing import Union, Optional

from apscheduler.schedulers.background import BackgroundScheduler
import torch
from apscheduler.schedulers.base import STATE_STOPPED
import logging

logger = logging.getLogger(__name__)


class SleepyModule(torch.nn.Module):

    def __init__(self,
                 now_device: Union[torch.device, str],
                 module: torch.nn.Module,
                 interval: int,
                 rest_device: Optional[Union[torch.device, str]] = None,
                 active_device: Optional[Union[torch.device, str]] = None,
                 time_immediately: bool = False,
                 verbose_log: bool = False):
        super().__init__()
        self.mod: torch.nn.Module = module
        self.verbose_log = verbose_log
        self.now_device: torch.device = now_device

        if active_device is None:
            self.active_device: torch.device = now_device
        elif isinstance(active_device, str):
            self.active_device: torch.device = torch.device(active_device)
        else:
            self.active_device: torch.device = active_device

        if rest_device is None:
            self.rest_device: torch.device = torch.device("cpu")
        elif isinstance(rest_device, str):
            self.rest_device: torch.device = torch.device(rest_device)
        else:
            self.rest_device: torch.device = rest_device

        self.last_access_time: datetime = datetime.now()
        self.interval: timedelta = timedelta(seconds=interval)

        def move_to_rest_device():
            now = datetime.now()
            not_move_before = self.last_access_time + self.interval
            # if no need to back off
            if now > not_move_before:
                self.to(rest_device)
                self.now_device = self.rest_device
                if self.verbose_log:
                    logger.info(f"Moved module to {self.now_device}")

        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(func=move_to_rest_device, trigger="interval", seconds=interval)
        if time_immediately:
            self._scheduler.start()

    def forward(self, *args, **kwargs):
        if self._scheduler.state == STATE_STOPPED:
            self._scheduler.start()
        if self.now_device == self.rest_device:
            self.to(self.active_device)
            self.now_device = self.active_device
            if self.verbose_log:
                logger.info(f"Moved module to {self.now_device}")

        # auto back off
        self.last_access_time = datetime.now()
        return self.mod(*args, **kwargs)
