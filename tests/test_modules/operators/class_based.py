"""Collection of test methods/operators for in-class access."""

import inspect as _inspect


class ClassNoParams():
    """Class with no parameters."""

    def __init__(self):
        """Class with no parameters"""
        print("Init test class with no params")

    def operator_no_params_no_shared_no_return(self):
        """Operator with no parameters, no shared and no return"""
        print(_inspect.currentframe().f_code.co_name)

    def operator_no_shared_no_return(self, value_str: str, value_int: int):
        """Operator with parameters, no shared and no return"""
        print(_inspect.currentframe().f_code.co_name,\
              ": str=", value_str,\
              "int=", value_int)

    def operator_no_return(self,
                           value_str: str,
                           governor_shared: dict,
                           me_: str = _inspect.currentframe().f_code.co_name):
        """Operator with parameters, shared and no return"""

        # Modify
        if len(governor_shared) > 0:
            governor_shared[next(iter(governor_shared))] = value_str

        print(me_,\
              ": str=", value_str,\
              "shared=", governor_shared)

    def operator(self,value_str: str,
                governor_shared: dict):
        """Operator with parameters, shared and return"""

        self.operator_no_return(value_str,
                                governor_shared,
                                me_=_inspect.currentframe().f_code.co_name)
        return True


class ClassWithParams(ClassNoParams):
    """Class with no parameters."""

    def __init__(self, init_str: str, init_int: int):
        """Class with no parameters"""
        super(ClassNoParams, self).__init__()
        print("Init test class with params:",
              "str=", init_str,
              "int=", init_int)

    def __getattr__(self, name):
        if hasattr(ClassNoParams, name):
            return getattr(ClassNoParams, name)
        else:
            return self.__getattribute__(name)
