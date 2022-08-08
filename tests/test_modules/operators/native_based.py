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
                       shared_param_1: str,
                       me_: str = None):
    """Operator with parameters, shared and no return"""
    if me_ is None:
        me_ = _inspect.currentframe().f_code.co_name
    print(me_,\
          ": str=", value_str,\
          "shared_param_1=", shared_param_1)


def operator(value_str: str,
             shared_param_2: str) -> bool:
    """Operator with parameters, shared and return"""

    operator_no_return(value_str,
                       shared_param_2,
                       me_=_inspect.currentframe().f_code.co_name)
    return True


def operator_multi_share(value_str: str,
                         shared_param_1: str,
                         shared_param_2: str):
    """Operator with parameters, multi-shared and no return"""
    print(_inspect.currentframe().f_code.co_name,\
          ": str=", value_str,\
          "shared_param_1=", shared_param_1,\
          "shared_param_2=", shared_param_2)


def operator_add_to_shared(value_to_add: int,
                           shared_param_3: int):
    """Operator with parameters with returned addition to shared parameter."""
    print(_inspect.currentframe().f_code.co_name,\
          ": value_to_add=", value_to_add,\
          "shared_param_3=", shared_param_3)
    return shared_param_3 + value_to_add
