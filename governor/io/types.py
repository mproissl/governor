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
    DICT = 3


def config_type_description():
    """Configuration type descriptions."""
    return {
        ConfigType.YAML: "YAML File Configuration.",
        ConfigType.JSON: "JSON File Configuration.",
        ConfigType.JSON_STRING: "JSON-String Configuration.",
        ConfigType.DICT: "Dictionary Configuration.",
    }


def config_header_parameters():
    """Configuration header parameters with descriptions."""
    return {
        "name": {
            "description": "Name of the configuration, e.g. with reference "\
                           "to its use.",
            "dtype": str,
            "default": None
        },

        "description": {
            "description": "Longer description of the configuration or use "\
                           "case purpose.",
            "dtype": str,
            "default": None
        },

        "enable_multiprocessing": {
            "description": "Flag to create multiple processes to run "\
                           "operators in parallel. Default: True",
            "dtype": bool,
            "default": True
        },

        "shared_data": {
            "description": "Dictionary with globally shared data such as "\
                           "flags, static parameters, or any other data.",
            "dtype": dict,
            "default": None
        },
    }


def config_payload_operator_parameters():
    """Configuration operator parameters with descriptions."""
    return {
        "id_":
            "Globally unique identifier of operator. Default: "\
            "automatically generated.",

        "name":
            "Name of operator and thus Python method name to run.",

        "label":
            "Custom label attached to this operator, which may describe "\
            "the operator better than the name.",

        "module_path":
            "Python path to operator module using dots convention.",

        "class_name":
            "Name of the class containing the operator method to run.",

        "class_params":
            "Dictionary of parameter settings to pass to class "\
            "containing the operator method using the keys for "\
            "parameter names and respective values for parameter "\
            "values.",

        "dedicated_input_params":
            "Dictionary of dedicated parameter "\
            "settings to pass to the operator method "\
            "using the keys for parameter names and "\
            "respective values for parameter values.",

        "shared_input_params":
            "Either the name of an existing globally-"\
            "shared object or new object of the tuple "\
            "shape ('OBJECT_NAME', initial-value).",

        "save_output":
            "If the operator has a return value, this flag can "\
            "be set to save the response. Default: False",

        "shared_output_name":
            "If save_output is set to True, the response "\
            "can be shared with other operators given "\
            "this globally-unique user-defined name.",

        "run_after":
            "Command to run this operator after completion of other "\
            "operator(s) given one (String) or more (list) of id_ "\
            "values assigned to the respective operators. If this "\
            "parameter is not set, operators are executed in the "\
            "order they appear in the configuration.",

        "run_after_parallel":
            "Boolean flag to allow parallel execution of "\
            "this operator if more than one run_after "\
            "id_ has been set. Default: False",

        "group":
            "User-defined group name which adds this operator to a "\
            "group of other operators, which belong together and "\
            "can be referenced as one larger operator.",

        "repeat":
            "Number of times to run this operator. Default: 1",

        "dedicated_input_variations":
            "Dictionary of input parameter variations with the name of the "\
            "parameter as key and a dictionary as value with either 'from', "\
            "'to', 'step_size' for numerical settings or 'list' for a list "\
            "of any values.",

        "run_synchronized_input_variations:":
            "Boolean flag to indicate if parameter values specified in "\
            "'dedicated_input_variations' shall be varied all at once, "\
            "which requires that the length must be equal over all variation "\
            "instructions, or one parameter is varied at a time and thus all "\
            "permutations are being run. Default: False",

        "run_group_level_variations":
            "Boolean flag to run variations specified in "\
            "'dedicated_input_variations' after running all other operators "\
            "in the 'group'. Default: False"

    }


def config_payload_variation_parameters():
    """Configuration variation parameters with descriptions."""
    return {
        "repeat_groups":
            "Number of times to run a group of operators. Default: 1",

        "group_input_variations":
            "Dictionary of input parameter variations to apply to operators "\
            "belonging to the respective group using the following structure: "\
            "GROUP_NAME: PARAM_NAME: (dict with 'from', 'to', 'step_size' "\
            "for numerical settings or 'list' for a list of any values).",

        "run_synchronized_input_variations:":
            "Boolean flag to indicate if parameter values specified in "\
            "'group_input_variations' shall be varied all at once, "\
            "which requires that the length must be equal over all variation "\
            "instructions, or one parameter is varied at a time and thus all "\
            "permutations are being run. Default: False"
    }


def config_payload_variation_options():
    """Configuration options for variation parameters."""
    return {
        "range_based":
            {
                "from": float,
                "to": float,
                "step_size": float
            },

        "list_based":
            {
                "list": list
            }
    }
