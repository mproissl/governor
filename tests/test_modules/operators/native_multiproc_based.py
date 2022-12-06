"""Collection of multiproc test methods/operators for native/direct access."""

import inspect as _inspect
from time import sleep
from datetime import datetime


def job_noreturn(id_: str, iterations: int, process_time_sec: int):
    """Task with no shared and no return"""
    print(datetime.now().strftime("%H:%M:%S")+
          " START "+
          id_+ ": "+
          _inspect.currentframe().f_code.co_name+
          " N="+str(iterations)+
          " T="+str(process_time_sec)+"s",
          flush=True
         )
    for _ in range(iterations):
        sleep(process_time_sec)
    print(datetime.now().strftime("%H:%M:%S")+
          " END "+
          id_,
          flush=True)

def job_return(id_: str, process_time_sec: int, msg: str):
    """Task with no shared and return"""
    print(datetime.now().strftime("%H:%M:%S")+
          " START "+
          id_+ ": "+
          _inspect.currentframe().f_code.co_name+
          " T="+str(process_time_sec)+"s",
          flush=True
         )
    sleep(process_time_sec)
    print(datetime.now().strftime("%H:%M:%S")+
          " END "+
          id_,
          flush=True)
    return msg
