# MIT License
#
# Copyright (c) 2022 Manuel Proissl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Operator abstraction of any Python code."""

# Third-Party Dependencies
from importlib import import_module as _import
from timeit import default_timer as _timer

# Local Dependencies
from governor.objects.types import OperatorState as _OperatorState


class Operator():
    """Node of directed graph representing an operator."""

    def __init__(self,
                 # Required inputs
                 id_: str,
                 name: str,
                 module_path: str,
                 # Optional inputs
                 label: str = None,
                 class_name: str = None,
                 class_params: dict = None,
                 input_params: dict = None,
                 input_modifiable: dict = None,
                 operator_: object = None
                ):
        """Initialize a new operator.

        Args:
            id_: Unique graph-wide operator identifier, which is usually set
                 by the Controller that assures uniqueness.
            name: User-defined name of the operator, which does not have to
                  comply to uniqueness within the graph but reflects the
                  name of the method to run in the respective Python module.
            module_path: Python path to operator module using dots or file
                         path to Python script using OS-specific delimeters.
            label: (Optional) user-defined label attached to this operator,
                   which may describe the operator better than the :name:
            class_name: (Optional) Name of the class that contains the operator
                        method :name:.
            class_params: (Optional) Dictionary of parameters to initialize the
                          class specified with :class_name:
            input_params: (Optional) Dictionary of parameter settings to pass
                          to operator method :name:.
            input_modifiable: (Optional) Dictionary that may be modified by the
                              operator method :name:, which must contain the
                              parameter named by "governor_shared".
            operator_: (Optional) Direct-pass of operator in case reloading
                       not needed, which is currently handled by the graph
                       controller.
        """
        # Private vars by class args
        self._id = id_
        self._name = name
        self._module_path = module_path
        self._label = label
        self._input_params = input_params
        self._input_modifiable = input_modifiable

        # Private vars by init
        self._me = "Operator():"
        self._operator = None
        self._operator_ref = ""
        self._state = _OperatorState.OFFLINE
        self._exception = ""
        self._start_time = 0.
        self._end_time = 0.
        self._duration_sec = 0.
        self._response = None

        try:
            # Load new operator
            if operator_ is None:

                # Operator not contained in class
                if class_name is None:

                    # Loading operator directly
                    self._operator_ref = f"{module_path}.{name}"
                    self._operator = getattr(_import(module_path), name)

                # Operator contained in class without parameters
                elif class_params is None:

                    # Access to operator via class initialization
                    # without parameters passed to the constructor
                    self._operator_ref = f"{module_path}.{class_name}().{name}"
                    self._operator = \
                        getattr(
                            getattr(
                                _import(module_path), class_name)(), name)

                # Operator contained in class with parameters
                else:

                    # Access to operator via class initialization
                    # with parameters passed to the constructor
                    self._operator_ref = f"{module_path}.{class_name}"\
                                            "(**class_params).{name}"
                    self._operator = \
                        getattr(
                            getattr(
                                _import(module_path),
                                class_name)(**class_params), name)

            # Use provided operator
            else:
                self._operator = operator_

        except (ImportError, AttributeError) as err:

            # Set error state
            self._state = _OperatorState.ERROR

            # Keep exception trace
            self._exception = repr(err).replace("\n", " ")

            # Re-raise
            raise ImportError(f"{self._me} Failed loading operator"\
                               " '{self._operator_ref}'.") from err

    @property
    def id(self) -> str:
        """Unique identifier of operator."""
        return self._id

    @property
    def name(self) -> str:
        """Name of operator."""
        return self._name

    @property
    def module_path(self) -> str:
        """Path to operator module."""
        return self._module_path

    @property
    def label(self) -> str:
        """User-defined operator label."""
        return self._label

    @property
    def state(self) -> _OperatorState:
        """Current state of operator."""
        return self._state

    @property
    def exception(self) -> str:
        """Current raised exception string."""
        return self._exception

    def run(self):
        """Run operator."""
        try:
            # Run operator without input parameters
            if self._input_params is None:
                self._run_init()
                self._response = self._operator()
                self._run_close()

            # Run operator with input parameters
            elif self._input_modifiable is None:
                self._run_init()
                self._response = self._operator(**self._input_params)
                self._run_close()

            # Run operator with input parameters and modifiable
            else:
                self._run_init()
                self._response = self._operator(
                    **self._input_params,
                    governor_shared = self._input_modifiable
                )
                self._run_close()

        except Exception as err:

            # Set error state
            self._state = _OperatorState.ERROR

            # Keep exception trace
            self._exception = repr(err).replace("\n", " ")

            # Re-raise
            raise RuntimeError(f"{self._me} Failed running operator"\
                                       " '{self._operator_ref}'.") from err

    def _run_init(self):
        """Update setting before running operator."""

        # Update state
        self._state = _OperatorState.ONLINE

        # Capture start time
        self._start_time = _timer()

    def _run_close(self):
        """Update setting after running operator."""

        # Update state
        self._state = _OperatorState.COMPLETED

        # Capture start time
        self._end_time = _timer()
        self._duration_sec = (self._end_time - self._start_time)

    def reset(self):
        """Reset operator for reuse."""
        self._state = _OperatorState.OFFLINE
        self._exception = ""
        self._start_time = 0.
        self._end_time = 0.
        self._duration_sec = 0.
        self._response = None
