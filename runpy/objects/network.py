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
"""Network abstraction of any operators."""


class Network():
    """Directed graph of operators representing a network."""

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
                              parameter named by "runpy_shared".
            operator_: (Optional) Direct-pass of operator in case reloading
                       not needed, which is currently handled by the graph
                       controller.
        """
