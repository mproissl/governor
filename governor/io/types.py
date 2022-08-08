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
        "id_": {
            "description": "Globally unique identifier of operator. Default: "\
                           "automatically generated.",
            "dtype": str,
            "default": None
        },

        "name": {
            "description": "Name of operator and thus Python method name to "\
                           "run.",
            "dtype": str,
            "default": None
        },

        "label": {
            "description": "Custom label attached to this operator, which "\
                           "may describe the operator better than the name.",
            "dtype": str,
            "default": None
        },

        "module_path": {
            "description": "Python path to operator module using dots "\
                           "convention.",
            "dtype": str,
            "default": None
        },

        "class_name": {
            "description": "Name of the class containing the operator method "\
                           "to run.",
            "dtype": str,
            "default": None
        },

        "class_params": {
            "description": "Dictionary of parameter settings to pass to "\
                           "class containing the operator method using the "\
                           "keys for parameter names and respective values "\
                           "for parameter values.",
            "dtype": dict,
            "default": None
        },

        "dedicated_input_params": {
            "description": "Dictionary of dedicated parameter settings to "\
                           "pass to the operator method using the keys for "\
                           "parameter names and respective values for "\
                           "parameter values.",
            "dtype": dict,
            "default": None
        },

        "shared_input_params": {
            "description": "Either the name of an existing globally-shared"\
                           "object, a list of these names if more than one "\
                           "or a set of new objects in dictionary format: "\
                           "'OBJECT_NAME': initial-value.",
            "dtype": (str, list, dict),
            "default": None
        },

        "shared_input_init_only": {
            "description": "If shared_input_params are given for "\
                           "initialization, i.e. in form of a dictionary, "\
                           "this flag can be set to only allow this "\
                           "operator for one-time use. Default: False",
            "dtype": bool,
            "default": False
        },

        "save_output": {
            "description": "If the operator has a return value, this flag "\
                           "can be set to save the response. Default: False",
            "dtype": bool,
            "default": False
        },

        "shared_output_name": {
            "description": "If save_output is set to True, the response can "\
                           "be shared with other operators given this "\
                           "globally-unique user-defined name. In case the "\
                           "save_output is set to True, but no name is "\
                           "given, then the operator id_ is used.",
            "dtype": str,
            "default": None
        },

        "run_after": {
            "description": "Command to run this operator after completion of "\
                           "other operator(s) given one (String) or more "\
                           "(list) of id_ values assigned to the respective "\
                           "operators. If this parameter is not set, "\
                           "operators are executed in the order they appear "\
                           "in the configuration.",
            "dtype": (str, list),
            "default": None
        },
#
#        "run_after_parallel":
#            "Boolean flag to allow parallel execution of "\
#            "this operator if more than one run_after "\
#            "id_ has been set. Default: False",

        "group": {
            "description": "User-defined group name which adds this operator "\
                           "to a group of other operators, which belong "\
                           "together and can be referenced as one larger "\
                           "operator.",
            "dtype": str,
            "default": None
        },

        "repeat": {
            "description": "Number of times to run this operator. Default: 1",
            "dtype": int,
            "default": 1
        },

        "reinitialize_in_repeats": {
            "description": "Flag to reinitialize operator in repetitive use. "\
                           "Default: True",
            "dtype": bool,
            "default": True
        },

        "dedicated_input_variations": {
            "description": "Dictionary of input parameter variations with "\
                           "the name of the parameter as key and a "\
                           "dictionary as value with either 'from', 'to', "\
                           "'step_size' for numerical settings or 'list' for "\
                           "a list of any values.",
            "dtype": dict,
            "default": None
        },

        "run_synchronized_input_variations:": {
            "description": "Boolean flag to indicate if parameter values "\
                           "specified in 'dedicated_input_variations' shall "\
                           "be varied all at once, which requires that the "\
                           "length must be equal over all variation "\
                           "instructions, or one parameter is varied at a "\
                           "time and thus all permutations are being run. "\
                           "Default: False",
            "dtype": bool,
            "default": False
        },

        "run_group_level_variations": {
            "description": "Boolean flag to run variations specified in "\
                           "'dedicated_input_variations' after running all "\
                           "other operators in the 'group'. Default: False",
            "dtype": bool,
            "default": False
        }
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


def get_config_values(method_name: str, attribute_name: str):
    """Extract value from config and provide as dictionary."""

    # Vars
    extract = {}
    supported = [
        "config_header_parameters()",
        "config_payload_operator_parameters()",
    ]

    # Evaluate
    try:
        # pylint: disable=eval-used
        config = eval(method_name) if method_name in supported else None
        # pylint: enable=eval-used
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        config = None
        pass

    # Extract
    if config is not None:
        for key in config:
            extract[key] = config[key][attribute_name]
    return extract
