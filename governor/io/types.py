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
"""Common type definitions used by i/o methods."""

# Dependencies
from enum import Enum as _Enum, unique as _unique


@_unique
class ConfigType(_Enum):
    """Configuration source types."""
    YAML = 0
    JSON = 1
    JSON_STRING = 2


def config_type_description():
    """Configuration type descriptions."""
    return {
        ConfigType.YAML: "YAML File Configuration.",
        ConfigType.JSON: "JSON File Configuration.",
        ConfigType.JSON_STRING: "JSON-String Configuration."
    }


def config_header_parameters():
    """Configuration header parameters with descriptions."""
    return {
        "name": "Name of the configuration, e.g. with reference to its use.",
        
        "description": "Longer description of the configuration or use case purpose.",
        
        "enable_multiprocessing": "Flag to create multiple processes to run operators in parallel. Default: True",
        

    }


def config_payload_operator_parameters():
    """Configuration operator parameters with descriptions."""
    return {
        "id_": "Globally unique identifier of operator. Default: automatically generated.",
        
        "name": "Name of operator and thus Python method name to run.",
        
        "label": "Custom label attached to this operator, which may describe the operator better than the name.",
        
        "module_path": "Python path to operator module using dots convention.",
        
        "class_name": "Name of the class containing the operator method to run.",
        
        "class_params": "Dictionary of parameter settings to pass to class containing the operator method using the keys for parameter names and respective values for parameter values.",
        
        "dedicated_input_params": "Dictionary of dedicated parameter settings to pass to the operator method using the keys for parameter names and respective values for parameter values.",
        
        "shared_input_params": "Either the name of an existing globally-shared object or new object of the tuple shape ('OBJECT_NAME', initial-value).",
        
        "save_output": "If the operator has a return value, this flag can be set to save the response. Default: False",
        
        "shared_output_name": "If save_output is set to True, the response can be shared with other operators given this globally-unique user-defined name."
    }
