"""Collection of multiproc test methods/operators for native/direct access."""

import inspect as _inspect
from time import sleep
from datetime import datetime


def operator_task(iterations: int, process_time_sec: int):
    """Task with no shared and no return"""
    for i in range(0, iterations):
        sleep(process_time_sec)
        print(_inspect.currentframe().f_code.co_name, i, datetime.now())

def operator_post(msg: str):
    """Post-Task with no shared and no return"""
    print(_inspect.currentframe().f_code.co_name, msg)
