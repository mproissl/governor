"""Collection of test methods/operators for native/direct access."""

import inspect as _inspect

def operator_no_params_no_shared_no_return():
    """Operator with no parameters, no shared and no return"""
    print(_inspect.currentframe().f_code.co_name)


def operator_no_shared_no_return(value_str: str, value_int: int):
    """Operator with parameters, no shared and no return"""
    print(_inspect.currentframe().f_code.co_name,\
          ": str=", value_str,\
          "int=", value_int)


def operator_no_return(value_str: str,
                       governor_shared: dict,
                       me_: str = _inspect.currentframe().f_code.co_name):
    """Operator with parameters, shared and no return"""

    # Modify
    if len(governor_shared) > 0:
        governor_shared[next(iter(governor_shared))] = value_str

    print(me_,\
          ": str=", value_str,\
          "shared=", governor_shared)


def operator(value_str: str,
             governor_shared: dict):
    """Operator with parameters, shared and return"""

    operator_no_return(value_str,
                       governor_shared,
                       me_=_inspect.currentframe().f_code.co_name)
    return True
